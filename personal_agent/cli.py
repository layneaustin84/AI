"""
Personal Agent CLI
Main command-line interface for the personal agent
"""

import click
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from config_loader import ConfigLoader
from gemini_wrapper import GeminiWrapper
from file_handler import FileHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonalAgent:
    """Main personal agent class."""

    def __init__(self):
        """Initialize the personal agent."""
        try:
            self.config = ConfigLoader()
            self.gemini = GeminiWrapper(self.config.get_api_key())
            self.file_handler = FileHandler(self.config)
            logger.info("Personal Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Personal Agent: {e}")
            raise


@click.group()
def cli():
    """Personal Agent - Your AI-powered text transformation tool."""
    pass


@cli.command()
@click.argument('text', required=False)
@click.option('--tone', '-t', default='friendly', help='Tone profile to use')
@click.option('--file', '-f', type=click.Path(exists=True), help='Read text from file')
@click.option('--doc-type', '-d', default='general', help='Document type for auto-profile selection')
@click.option('--instruction', '-i', help='Custom instruction to append to tone profile')
@click.option('--output', '-o', type=click.Path(), help='Save output to file')
def humanize(text: str, tone: str, file: Optional[str], doc_type: str, instruction: Optional[str], output: Optional[str]):
    """
    Humanize text using a specific tone profile.

    Examples:
        humanize "Draft OSHA report"
        humanize --file report.txt --tone osha_formal
        humanize --file email.txt --tone linkedin_casual --output humanized.txt
    """
    try:
        agent = PersonalAgent()

        # Load text
        if file:
            input_text = Path(file).read_text()
            logger.info(f"Loaded text from {file}")
        elif text:
            input_text = text
        else:
            click.echo("Error: Please provide text or use --file option")
            sys.exit(1)

        # Get tone profile
        if tone and tone in agent.config.tone_profiles:
            profile = agent.config.get_tone_profile(tone)
            click.echo(f"Using tone profile: {profile['name']}")
        else:
            # Try to get default for document type
            default_tone = agent.config.get_default_profile_for_type(doc_type)
            profile = agent.config.get_tone_profile(default_tone)
            click.echo(f"Using default tone for {doc_type}: {profile['name']}")

        # Humanize
        click.echo("🤖 Humanizing text...")
        humanized = agent.gemini.humanize_text(input_text, profile, instruction)

        # Output
        if output:
            Path(output).write_text(humanized)
            click.echo(f"✅ Output saved to: {output}")
        else:
            click.echo("\n" + "="*60)
            click.echo(humanized)
            click.echo("="*60)

        # Log the operation
        agent.file_handler.log_operation(
            operation="humanize",
            input_length=len(input_text),
            output_length=len(humanized),
            tone_profile=tone or default_tone,
            doc_type=doc_type
        )

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Humanize failed: {e}")
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--tone', '-t', default='friendly', help='Tone profile to use')
@click.option('--pattern', '-p', default='*.txt', help='File pattern to match')
@click.option('--output-dir', '-o', type=click.Path(), help='Directory for output files')
@click.option('--preserve-names', is_flag=True, help='Preserve original filenames (adds suffix)')
def batch(directory: str, tone: str, pattern: str, output_dir: Optional[str], preserve_names: bool):
    """
    Batch humanize multiple files in a directory.

    Examples:
        batch ./documents --tone osha_formal
        batch ./reports --pattern "*.md" --output-dir ./humanized
    """
    try:
        agent = PersonalAgent()

        # Get output directory
        out_dir = Path(output_dir) if output_dir else agent.config.get_output_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

        # Get files
        source_dir = Path(directory)
        files = list(source_dir.glob(pattern))

        if not files:
            click.echo(f"No files matching pattern '{pattern}' found in {directory}")
            return

        click.echo(f"🔄 Processing {len(files)} files with tone: {tone}")

        # Get tone profile
        profile = agent.config.get_tone_profile(tone)

        # Process files
        results = []
        for i, file_path in enumerate(files, 1):
            try:
                click.echo(f"  [{i}/{len(files)}] Processing {file_path.name}...", nl=False)
                input_text = file_path.read_text()

                humanized = agent.gemini.humanize_text(input_text, profile)

                # Save output
                if preserve_names:
                    output_name = file_path.stem + f"_humanized{file_path.suffix}"
                else:
                    output_name = file_path.name

                output_path = out_dir / output_name
                output_path.write_text(humanized)

                click.echo(f" ✅")
                results.append({
                    'file': file_path.name,
                    'status': 'success',
                    'output': str(output_path)
                })

            except Exception as e:
                click.echo(f" ❌ ({e})")
                results.append({
                    'file': file_path.name,
                    'status': 'failed',
                    'error': str(e)
                })

        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        click.echo(f"\n✅ Completed: {successful}/{len(files)} files processed")
        click.echo(f"📁 Output saved to: {out_dir}")

    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def profiles():
    """List all available tone profiles."""
    try:
        agent = PersonalAgent()
        profiles = agent.config.list_tone_profiles()

        click.echo("\n📋 Available Tone Profiles:\n")
        for name, description in profiles.items():
            click.echo(f"  • {name}")
            click.echo(f"    {description}\n")

    except Exception as e:
        logger.error(f"Failed to list profiles: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def types():
    """List all document types and their default profiles."""
    try:
        agent = PersonalAgent()
        doc_types = agent.config.list_document_types()

        click.echo("\n📑 Document Types & Defaults:\n")
        for doc_type, default_profile in doc_types.items():
            click.echo(f"  • {doc_type}")
            click.echo(f"    Default profile: {default_profile}\n")

    except Exception as e:
        logger.error(f"Failed to list document types: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    click.echo("Personal Agent v1.0.0")
    click.echo("Powered by Google Gemini API")


@cli.command()
@click.argument('text')
@click.option('--length', '-l', default='short', type=click.Choice(['short', 'medium', 'long']),
              help='Summary length')
def summarize(text: str, length: str):
    """
    Summarize text to key points.

    Examples:
        summarize "Your text here"
        summarize "Text to summarize" --length medium
    """
    try:
        agent = PersonalAgent()
        click.echo("📝 Summarizing text...")
        summary = agent.gemini.summarize_text(text)

        click.echo("\n" + "="*60)
        click.echo(summary)
        click.echo("="*60)

    except Exception as e:
        logger.error(f"Summarize failed: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('text')
def takeaways(text: str):
    """
    Extract key takeaways from text.

    Examples:
        takeaways "Your text here"
    """
    try:
        agent = PersonalAgent()
        click.echo("🎯 Extracting takeaways...")
        result = agent.gemini.extract_takeaways(text)

        click.echo("\n" + "="*60)
        click.echo(result)
        click.echo("="*60)

    except Exception as e:
        logger.error(f"Takeaways extraction failed: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
