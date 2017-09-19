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

gulp.task('copy-scripts', function(){

    let destinationPath = distPath +'js/',
        jsLibScripts = [
            nodeModulesPath + 'jquery/dist/jquery.min.js',
            nodeModulesPath + 'bootstrap/dist/js/bootstrap.min.js',
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
        'copy-fonts',
        'copy-styles',
        'compile-styles'
    ]);
});