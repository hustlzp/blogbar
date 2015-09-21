var gulp = require('gulp');
var tap = require('gulp-tap');
var path = require('path');
var less = require('gulp-less');
var concat = require('gulp-concat');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');

var cssRoot = './application/static/css';
var jsRoot = './application/static/js';

gulp.task('macros-css', function () {
    var stream = gulp.src(path.join(cssRoot, '**/_*.less'))
        .pipe(less({
            paths: [cssRoot]
        }))
        .pipe(concat('macros.css'));

    if (process.env.MODE === 'PRODUCTION') {
        stream = stream.pipe(minifyCss({compatibility: 'ie8'}));
    }

    return stream.pipe(gulp.dest('./output/'));
});

gulp.task('macros-js', function () {
    var stream = gulp.src(path.join(jsRoot, '**/_*.js'))
        .pipe(concat('macros.js'));

    if (process.env.MODE === 'PRODUCTION') {
        stream = stream.pipe(uglify());
    }

    return stream.pipe(gulp.dest('./output/'));
});

gulp.task('default', ['macros-css', 'macros-js'], function () {
});
