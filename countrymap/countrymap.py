"""
"""

import shapefile
import os

import wget
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import numpy as np
from matplotlib.collections import LineCollection



class Map(object):
    def __init__(self, region=None):
        """
        init class

        Parameters

        region : str or user defined dictionary
        """
        self._set_region(region)
        self._default_shp = 'TM_WORLD_BORDERS-0.3.shp'


    def _set_region(self, region):
        assert region is not None, 'Region needs to be specified!'
        self._set_default_regions()
        if type(region) is str:
            # use default region
            if region in self.regions.keys():
                self.x1 = self.regions[region]['lon1']
                self.x2 = self.regions[region]['lon2']
                self.y1 = self.regions[region]['lat1']
                self.y2 = self.regions[region]['lat2']
                self.label = region
            else:
                print('ERROR: region is not in list of default regions')
                assert False
        else:
            assert len(region.keys()) == 1, 'Only a single region can be specified!'
            k = region.keys()[0]
            self.x1 = region[k]['lon1']
            self.x2 = region[k]['lon2']
            self.y1 = region[k]['lat1']
            self.y2 = region[k]['lat2']
            self.label = k


    def _set_default_regions(self):
        r_eur = {'lon1' : -30., 'lon2' : 35., 'lat1' : 30., 'lat2' : 72.}
        self.regions = {'europe' : r_eur}

    def _download_shape(self):
        """
        download default shapefile

        for some reason this does not work in automatic mode so far ...
        """
        url = 'http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip'
        filename = wget.download(url)

        # still need to implement unzi here


    def read_shape(self, shpname=None):
        if shpname is None:
            # set default shapename
            shpname = self._default_shp

        # check if shapefile existing
        if not os.path.exists(shpname):
            # in case that default is missing, try to download
            if shpname == self._default_shp:
                pass
            else:
                assert False, 'Can not continue with processing as shapefile not existing!'

        # read shapefile
        r = shapefile.Reader(shpname)
        #print r.fields
        self.shapes = r.shapes()
        self.records = r.records()


    def draw(self):
        self._draw_basic()


    def _draw_basic(self):
        """
        This functions draws and returns a map of Portugal, either just of the mainland or including the Azores and Madeira islands.
        """

        fig = plt.figure(figsize=(15.7,12.3))
        self.ax = fig.add_subplot(111)

        projection='merc'
        llcrnrlat=-80
        urcrnrlat=90
        llcrnrlon=-180
        urcrnrlon=180
        resolution='i'

        m = Basemap(projection=projection, llcrnrlat=self.y1, urcrnrlat=self.y2, llcrnrlon=self.x1,
                    urcrnrlon=self.x2, resolution=resolution, ax=self.ax)
        m.drawcoastlines()
        m.drawmapboundary()
        #m.drawcountries()
        #m.fillcontinents(color = '#C0C0C0')
        m.fillcontinents(color = 'lightgrey')

        self.m = m

    def draw_details(self, names=None, color='red'):

        names1 = []
        for n in names:
            names1.append(n.upper())

        for record, shape in zip(self.records,self.shapes):
            #read shape
            if len(shape.points) < 1:
                continue
            lons,lats = zip(*shape.points)
            data = np.array(self.m(lons, lats)).T

            #each shape may have different segments
            if len(shape.parts) == 1:
                segs = [data,]
            else:
                segs = []
                for i in range(1,len(shape.parts)):
                    index = shape.parts[i-1]
                    index2 = shape.parts[i]
                    segs.append(data[index:index2])
                segs.append(data[index2:])

            #draws the segments, and sets its properties. A colormap is used to get the gradient effect.
            lines = LineCollection(segs,antialiaseds=(1,))
            #lines.set_facecolors(cm.YlGn(record[-1]))
            if record[4].upper() in names1:
                lines.set_facecolors(color)
            lines.set_edgecolors('k')
            lines.set_linewidth(1)
            self.ax.add_collection(lines)
