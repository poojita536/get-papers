import typer
import pandas as pd
from get_papers.fetcher import fetch_pubmed_ids, fetch_details
from get_papers.parser import parse_articles

app = typer.Typer()

@app.command()
def main(
    query: str,
    file: str = typer.Option(None, "--file", "-f"),
    debug: bool = typer.Option(False, "--debug", "-d")
):
    if debug:
        typer.echo(f"Searching: {query}")

    ids = fetch_pubmed_ids(query)
    if not ids:
        typer.echo("No results.")
        return

    xml = fetch_details(ids)
    data = parse_articles(xml)

    if not data:
        typer.echo("No non-academic authors found.")
        return

    df = pd.DataFrame(data)
    if file:
        df.to_csv(file, index=False)
        typer.echo(f"Saved to {file}")
    else:
        typer.echo(df.to_string(index=False))

if __name__ == "__main__":
    app()
