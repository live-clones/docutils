# Source and destination file names
test_source = "data/footnote-targets.rst"
test_destination = "latex_footnotes.tex"

# Keyword parameters passed to publish_file()
writer = "latex"
settings_overrides = {
    'latex_footnotes': True,  # use LaTeX \footnote cmd
    'legacy_column_widths': False,
    'use_latex_citations': True,  # avoid FutureWarning
    }
