import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# -- General configuration ------------------------------------------------

extensions		= ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']
templates_path	= ['_templates']
source_suffix	= '.txt'
master_doc		= 'index'
project			= 'Microngo'
copyright		= '2019, Em Suryadi'
author			= 'Em Suryadi'
version			= '0.1.0'
release			= version
language		= 'en'

exclude_patterns		= ['_build', 'Thumbs.db', '.DS_Store']
pygments_style			= 'sphinx'
todo_include_todos		= False
autoclass_content		= 'both'
autodoc_member_order	= 'bysource'

# -- Options for HTML output ----------------------------------------------

html_theme			= 'flask'
html_static_path	= ['_static']
html_theme_options	= {
	"github_fork":			"emsuryadi/Microngo",
	"index_logo":			"logo.png",
	"index_logo_height":	"150px",
}