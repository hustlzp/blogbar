var gulp = require('gulp');
var tap = require('gulp-tap');
var path = require('path');
var less = require('gulp-less');
var concat = require('gulp-concat');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var plumber = require('gulp-plumber');
var gulpif = require('gulp-if');

var cssRoot = './application/static/css';
var jsRoot = './application/static/js';

gulp.task('macros-css', function () {
    return gulp
        .src(path.join(cssRoot, '**/_*.less'))
        .pipe(plumber())
        .pipe(less({
            paths: [cssRoot]
        }))
        .pipe(concat('macros.css'))
        .pipe(gulpif(inProduction, minifyCss({compatibility: 'ie8'})))
        .pipe(gulp.dest('./application/static/output/'));
});

gulp.task('macros-js', function () {
    return gulp
        .src(path.join(jsRoot, '**/_*.js'))
        .pipe(plumber())
        .pipe(concat('macros.js'))
        .pipe(gulpif(inProduction, uglify()))
        .pipe(gulp.dest('./application/static/output/'));
});

gulp.task('default', ['macros-css', 'macros-js'], function () {
});

gulp.task('watch', function () {
    gulp.watch(path.join(jsRoot, '**/_*.js'), ['macros-js']);
    gulp.watch(path.join(cssRoot, '**/_*.less'), ['macros-css']);
});

function inProduction() {
    return process.env.MODE === 'PRODUCTION';
}
