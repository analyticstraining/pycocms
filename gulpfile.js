/* jshint node: true */

'use strict';

let gulp = require('gulp'),
    streamqueue = require('streamqueue'),
    runSequence = require('run-sequence'),
    buildTools = require('gulp-load-plugins')(),
    del = require('del'),
    path = require('path'),
    _ = require('lodash'),
    glob = require('glob'),
    mapStream = require('map-stream');

let BUILD_RELEASE = false,
    packagesPath = [
        './package.json',
    ],
    nodeModulesPath = 'node_modules/',
    appFilespath = 'src/',
    distPath,
    outputFiles; 

function notpath(paths) {
    return (Array.isArray(paths) ? paths : [paths]).map(function (path) {
        return '!' + path;
    });
}

function deglob() {
    var syncGlob = glob.sync,
        patterns = _.flatten(arguments, true);

    return _.flatten(patterns.map(function (pattern) {
        return syncGlob(pattern).map(function (file) {
            return pattern.charAt(0) === '!' ? ('!' + file) : file;
        });
    }), true);
}

function createOutputFilesAndDistPath() {
    distPath = "pyGAE/dist/";
}

gulp.task('copy-fonts', function () {
    let fontFiles = [
            nodeModulesPath + 'bootstrap/dist/fonts/*.*',
            nodeModulesPath + 'font-awesome/fonts/*.*'
        ],
        destinationPath = distPath +'fonts/';

    return gulp
        .src(fontFiles)
        .pipe(buildTools.changed(destinationPath))
        .pipe(gulp.dest(destinationPath))
    ;
});

gulp.task('copy-styles', function() {
    let cssFiles = [
            nodeModulesPath + 'bootstrap/dist/css/bootstrap.min.css',
            nodeModulesPath + 'bootstrap/dist/css/bootstrap-theme.min.css',
            nodeModulesPath + 'font-awesome/css/font-awesome.min.css',
        ],
        destinationPath = distPath + 'css/';

    return gulp
        .src(cssFiles)
        .pipe(buildTools.changed(destinationPath))
        .pipe(gulp.dest(destinationPath))
    ;
});

gulp.task('copy-tinymce-plugins', function() {
    let jsFiles = [
            nodeModulesPath + 'tinymce/themes/modern/theme.min.js',
        ],
        destinationPath = distPath + 'js/themes/modern/';

    let pluginPath = nodeModulesPath + 'tinymce/plugins/';
    let pluginDstPath = distPath + 'js/plugins/';

    function addPlugin(name) {
        gulp.src([pluginPath + name + '/**.*' ]).pipe(buildTools.changed(pluginDstPath + name)).pipe(gulp.dest(pluginDstPath + name));
    }
    addPlugin('code');
    addPlugin('link');
    addPlugin('fullscreen');
    return gulp
        .src(jsFiles)
        .pipe(buildTools.changed(destinationPath))
        .pipe(gulp.dest(destinationPath))
    ;
});

gulp.task('copy-tinymce-styles', function() {
    let jsFiles = [
            nodeModulesPath + 'tinymce/skins/lightgray/**.*',
            nodeModulesPath + 'tinymce/skins/lightgray/**/**.*',
        ],
        destinationPath = distPath + 'js/skins/lightgray/';

    return gulp
        .src(jsFiles)
        .pipe(buildTools.changed(destinationPath))
        .pipe(gulp.dest(destinationPath))
    ;
});

gulp.task('copy-scripts', function(){

    let destinationPath = distPath +'js/',
        jsLibScripts = [
            nodeModulesPath + 'jquery/dist/jquery.min.js',
            nodeModulesPath + 'bootstrap/dist/js/bootstrap.min.js',
            nodeModulesPath + 'tinymce/tinymce.min.js',
            appFilespath + 'editor/content_editor.js'
        ];
    return gulp
        .src(jsLibScripts)
        .pipe(buildTools.changed(destinationPath))
        .pipe(gulp.dest(destinationPath))
    ;
});

gulp.task('compile-styles', function() {
    let appStyles = 'src/css/*.css',
        compiledStyles = distPath + 'css/app.min.css',
        concatOutputPath = path.dirname(compiledStyles),
        concatOutputFileName = path.basename(compiledStyles),
        styleFiles = deglob(
            appStyles
        ),
        minifyOptions = {
            advanced: false 
        };

    del(compiledStyles);
    del(compiledStyles + '.map');

    return gulp
        .src(styleFiles)
        .pipe(buildTools.sourcemaps.init({ loadMaps: true }))
            .pipe(buildTools.concat(concatOutputFileName))
            .pipe(BUILD_RELEASE ? buildTools.cleanCss({debug: true}, function(details) {
                console.log(details.name + ': ' + details.stats.originalSize, 'original size');
                console.log(details.name + ': ' + details.stats.minifiedSize, 'minified size');
              }) : buildTools.util.noop())
        .pipe(buildTools.sourcemaps.write('.'))
        .pipe(gulp.dest(concatOutputPath))
    ;
});

gulp.task('build-debug', function () {
    BUILD_RELEASE = true;
    createOutputFilesAndDistPath();
    runSequence.apply(this, [
        'copy-scripts',
        'copy-tinymce-plugins',
        'copy-tinymce-styles',
        'copy-fonts',
        'copy-styles',
        'compile-styles'
    ]);
});