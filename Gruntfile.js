module.exports = function(grunt) {

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        sass: {
            dev: {
                files: {
                    'SonidosLibres/static/css/output.css' : 'SonidosLibres/scss/output.scss'
                }
            }
        },
        watch: {
            options: {livereload: true},
            sass: {
                files: 'SonidosLibres/scss/**/*.scss',
                tasks: ['sass:dev']
            }
        },
    });

    grunt.registerTask('default', ['sass:dev']);
};

