def crop( large_rst, small_rst, output_path=None, compress=True, *args, **kwargs ):
	'''
	crop a larger raster by a smaller overlapping one.
	this function assumes the 2 rasters are in the same CRS
	arguments:
	----------
	large_rst = rasterio.raster object of the larger raster to be cropped
	small_rst = rasterio.raster object of the smaller raster used to crop the larger
	output_path = [optional] string path to directory to output the new GTiff created. 
		if None, it will be the directory of the large_rst.
	compress = boolean. Default = True.  If True lzw-compress. if False do not.
	returns:
	--------
	path to the newly generated cropped raster.  With the side-effect of outputting the 
	raster to disk.
	notes:
	------
	potential gotcha here is that it will only work on a single banded raster.
	'''
	import rasterio, os

	window = large_rst.window( *small_rst.bounds )
	crop_affine = large_rst.window_transform( window )
	window_arr = large_rst.read( 1, window=window )
	# make a new meta object to pass to the cropped rasterio
	height, width = window_arr.shape
	meta = small_rst.meta
	meta.update( affine=crop_affine,
				height=height,
				width=width,
				nodata=small_rst.nodata,
				crs=small_rst.crs,
				count=1,
				dtype=small_rst.dtypes[0] )

	output_name = os.path.basename( large_rst.name ).replace( '.tif', '_crop.tif' )

	if output_path:
		output_filename = os.path.join( output_path, output_name )
	else:
		output_path = os.path.dirname( large_rst.name )
		output_filename = os.path.join( output_path, output_name )

	with rasterio.open( output_filename, 'w', **meta ) as out:
		out.write( window_arr, 1 )
	return output_filename


if __name__ == '__main__':
	import glob
	import os
	import rasterio
	variable = ['pr','tas']
	template = '/Data/Base_Data/Climate/AK_CAN_2km/projected/AR5_CMIP5_models/rcp85/CCSM4/pr/pr_total_mm_AR5_CCSM4_rcp85_01_2006.tif'
	baseline_input = '/Data/Base_Data/Climate/AK_CAN_2km/historical/singleBand/prism/AK_CAN_2km_PRISM/AK_CAN_geotiffs/'
	for i in variable :
		l = glob.glob(os.path.join(baseline_input,i,'ak83albers','*.tif'))
		output_path = os.path.join('/workspace/Shared/Users/jschroder/LCC/baseline',i)
		if not os.path.exists( output_path ):
			os.makedirs( output_path )
		for files in l :
			crop(rasterio.open(files),rasterio.open( template),output_path)