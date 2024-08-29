from __future__ import annotations

from typing import Annotated, Optional

import typer
import secrets
import string

from pwgen import __version__

app = typer.Typer()


def version_callback(value: bool) -> None:
    if value:
        print(f"pwgen {__version__}")
        raise typer.Exit()


@app.command(name="pwgen")
def main(
    punctuation: Annotated[
        bool, typer.Option("-p", help="Include special characters")
    ] = False,
    quote_safe: Annotated[
        bool, typer.Option("-Q", help="Exclude characters that could escape quotes")
    ] = False,
    exclude: Annotated[
        str, typer.Option("-x", help="String of characters to exclude")
    ] = "",
    length: Annotated[int, typer.Option("-l", help="Password length")] = 16,
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
) -> None:
    """
    pwgen - Command-line password generation utility. Not for production-scale use.
    """
    if length < 8:
        typer.echo(
            "WARNING: short passwords are less secure, consider increasing the length of the password.",
            err=True,
        )

    alphabet = string.ascii_letters + string.digits
    if punctuation:
        alphabet += string.punctuation

    excluded_chars = set(exclude)
    if quote_safe:
        excluded_chars = excluded_chars.union(set(r"\'\"`"))

    if excluded_chars:
        alphabet = "".join(set(alphabet) - excluded_chars)

    typer.echo("".join(secrets.choice(alphabet) for _ in range(length)), nl=False)


if __name__ == "__main__":
    app()
