# extract_headings plugin for pelican

Any problems, please contact wilbur.ma@foxmail.com

This is a very simple pelican plugin which extracts the h1~h6 headings from a markdown document.

This plugin introduces two new member to the pelican content object:
*  html_headings: a list of heading objects like {tag: "h1", value: "Hello this is h1 heading"}
*  html_toc: table of contents build with the markdown headings, html unordered list style

## License

BSD (3-Clause) License. Please see LICENSE.txt for more details.

## Requirements

*  python-markdown: `pip install Markdown`

## Usage

First, clone the plugin repo to your plugin directory:

    git clone https://github.com/wilbur-ma/extract_headings ${PELICAN_PLUGIN_DIRECTORY}/extract_headings

Then add or update the `MD_EXTENSION` and `PLUGINS` variables in your pelican configuration:

    MD_EXTENSIONS = (['extra', 'codehilite', 'headerid'])
    PLUGINS = ['extract_headings']

## Use your own slugify function

You can define your own slugify function in your pelican configuration, e.g.:

    import md5 
    def my_slugify(value, sep):
        m = md5.new()
        m.update(value)
        return "toc_{}".format(m.digest().encode("hex"))
    from markdown.extensions.headerid import HeaderIdExtension
    MD_EXTENSIONS = ([HeaderIdExtension(configs=[('slugify', my_slugify)])])

You should tell the extrac_headings to use your slugify function by setting the `MY_SLUGIFY_FUNC` variable in your pelican configuration.

    MY_SLUGIFY_FUNC = my_slugify

## Thanks

*  extract_toc plugin
