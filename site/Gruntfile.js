module.exports = function(grunt) {
	// Project configuration.
	grunt.initConfig({
		purifycss: {
			options: {},
			target: {
				src: [
					'templates/*.html',
					'templates/fragment/*.html',
					'static/js/main.js',
					'static/Semantic-UI-1.8.1/dist/components/form.min.js',
					'static/Semantic-UI-1.8.1/dist/components/modal.min.js',
					'static/Semantic-UI-1.8.1/dist/components/dimmer.min.js',
					'static/Semantic-UI-1.8.1/dist/components/transition.min.js'
				],
				css: ['static/Semantic-UI-1.8.1/dist/semantic.css'],
				dest: 'static/Semantic-UI-1.8.1/dist/my_semantic.css'
			},
		},
		cssmin: {
			options: {
				shorthandCompacting: false,
				roundingPrecision: -1
			},
			target: {
				files: {
					'static/Semantic-UI-1.8.1/dist/my_semantic.min.css': 'static/Semantic-UI-1.8.1/dist/my_semantic.css'
				}
			}
		},
		uglify: {
			my_target: {
				files: {
					'static/js/main.min.js': 'static/js/main.js'
				},
			}
		},
	});

	// Load the plugin that provides the tasks.
	grunt.loadNpmTasks('grunt-purifycss');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-uglify');

	// Default task(s).
	grunt.registerTask('default', ['purifycss', 'cssmin', 'uglify']);
};