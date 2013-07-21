def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('reporting', parent_package, top_path)

    config.add_data_dir("template_reports")
    config.add_data_dir("css")
    config.add_data_dir("js")
    config.add_data_dir("icons")

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
