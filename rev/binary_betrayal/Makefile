dist_dir    := ./dist
build_dir   := ./build
binary_name := Which

all:
	pyinstaller --onefile src/Which.py --distpath $(dist_dir) --workpath $(build_dir) --clean --name $(binary_name)
	sha1sum $(dist_dir)/$(binary_name) > $(dist_dir)/$(binary_name).sha1.sig

clean:
	rm -rf $(dist_dir) $(build_dir)

