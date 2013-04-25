from os import stat
from os.path import relpath

import logging

from jinja2 import Environment, FileSystemLoader

def build_index(cities, index_dir, templates_dir):
    ''' Render index.html template and return its contents.
    '''
    logging.info('Building index page with %d cities' % len(cities))
    
    env = Environment(loader=FileSystemLoader(templates_dir))
    tpl = env.get_template('index.html')
    
    expanded_cities = [expand_city(city, index_dir) for city in cities]
    
    return tpl.render(cities=expanded_cities)

def expand_city(city, base_dir):
    ''' Return a copy of a city dictionary, with extra information for templates.
    '''
    osm_size = nice_size(stat(city['osm_path']).st_size)
    pbf_size = nice_size(stat(city['pbf_path']).st_size)
    o2p_size = nice_size(stat(city['o2p_path']).st_size)
    
    osm_path = relpath(city['osm_path'], base_dir)
    pbf_path = relpath(city['pbf_path'], base_dir)
    o2p_path = relpath(city['o2p_path'], base_dir)
    jpg_path = relpath(city['jpg_path'], base_dir)
    
    lat = city['top']/2 + city['bottom']/2
    lon = city['left']/2 + city['right']/2
    
    return dict(slug=city['slug'], name=city['name'],
                osm_path=osm_path, osm_size=osm_size,
                pbf_path=pbf_path, pbf_size=pbf_size,
                o2p_path=o2p_path, o2p_size=o2p_size,
                jpg_path=jpg_path, lat=lat, lon=lon)

def nice_size(size):
    ''' Return a nicely-formatted rendition of the file size.
    '''
    KB = 1024.
    MB = 1024. * KB
    GB = 1024. * MB
    TB = 1024. * GB

    if size < KB:
        size, suffix = size, 'B'
    elif size < MB:
        size, suffix = size/KB, 'KB'
    elif size < GB:
        size, suffix = size/MB, 'MB'
    elif size < TB:
        size, suffix = size/GB, 'GB'
    else:
        size, suffix = size/TB, 'TB'

    if size < 10:
        return '%.1f %s' % (size, suffix)
    else:
        return '%d %s' % (size, suffix)
