all: js

OUTPUT=js/main.js

js: src/*
	rm -f ${OUTPUT}
	cat src/Loader.js >> ${OUTPUT} && echo >> ${OUTPUT}
	cat src/Model.js >> ${OUTPUT} && echo >> ${OUTPUT}
	cat src/main.js >> ${OUTPUT} && echo >> ${OUTPUT}

