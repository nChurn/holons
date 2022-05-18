const gulp = require('gulp') //, debug = require('gulp-debug')
const sass = require('gulp-sass')
var cssimport = require('gulp-cssimport')
var browserSync = require('browser-sync').create()
var reload = browserSync.reload
var autoprefixer = require('gulp-autoprefixer')
var plumber = require('gulp-plumber')
var rigger = require('gulp-rigger')
var uglify = require('gulp-uglify')
var watch = require('gulp-watch')
// var concatCss = require('gulp-concat-css')

var path = {
  build: { // Тут мы укажем куда складывать готовые после сборки файлы
    html: 'build/',
    js: 'build/js/',
    css: 'build/css/',
    img: 'build/img/',
    fonts: 'build/fonts/'
  },
  prod: { // Тут мы укажем куда складывать готовые после сборки файлы
    html: 'website/static/build/',
    js: 'website/static/build/js/',
    css: 'website/static/build/css/',
    img: 'website/static/build/img/',
    fonts: 'website/static/build/fonts/'
  },
  src: { // Пути откуда брать исходники
    html: 'src/*.html', // Синтаксис src/*.html говорит gulp что мы хотим взять все файлы с расширением .html
    js: 'src/js/main.js', // В стилях и скриптах нам понадобятся только main файлы
    styles: 'src/sass/main.scss',
    img: 'src/img/**/*.*', // Синтаксис img/**/*.* означает - взять все файлы всех расширений из папки и из вложенных каталогов
    fonts: 'src/fonts/**/*.*',
    rawfonts: 'src/rawfonts/*.{ttf,otf}'
  },
  watch: { // Тут мы укажем, за изменением каких файлов мы хотим наблюдать
    html: 'src/**/*.html',
    js: 'src/js/**/*.js',
    style: 'src/sass/**/*.scss',
    img: 'src/img/**/*.*',
    fonts: 'src/fonts/**/*.*'
  },
  clean: './build'
}

gulp.task('browser-sync', function(done) { 
  browserSync.init({
    server: {
      baseDir: './build'
    },
    notify: false
  });
  
  browserSync.watch('./src').on('change', browserSync.reload);
  
  done()
}); 

gulp.task('html', function (done) {
  gulp.src(path.src.html) // Выберем файлы по нужному пути
    .pipe(plumber())
        // .pipe(debug())
        .pipe(rigger()) // Прогоним через rigger
        .pipe(gulp.dest(path.build.html)) // Выплюнем их в папку build
        .pipe(reload({stream: true})); // И перезагрузим наш сервер для обновлений

    done()
    }
);

gulp.task('js', function (done) {
  gulp.src(path.src.js) // Найдем наш main файл
    .pipe(plumber())
        .pipe(rigger()) // Прогоним через rigger
        // .pipe(sourcemaps.init()) // Инициализируем sourcemap
        // .pipe(uglify()) // Сожмем наш js
        // .pipe(sourcemaps.write()) // Пропишем карты
        .pipe(gulp.dest(path.prod.js)) // Выплюнем готовый файл в build
        .pipe(gulp.dest(path.build.js)) // Выплюнем готовый файл в build
        .pipe(reload({stream: true})); // И перезагрузим сервер

    done()
    }
);

gulp.task('styles', function (done) {
  gulp.src(path.src.styles) // Выберем наш main.scss
    .pipe(plumber())
        // .pipe(rigger()) // Прогоним через rigger
        .pipe(cssimport({}))
        .pipe(sass()) // Скомпилируем
        // .pipe(prefixer()) // Добавим вендорные префиксы
        // .pipe(cssmin()) // Сожмем
        .pipe(gulp.dest(path.prod.css)) // И в build
        .pipe(gulp.dest(path.build.css)) // И в build
        .pipe(reload({stream: true}));

        done()
    }
);

gulp.task('images', function (done) {
  gulp.src(path.src.img) // Выберем наши картинки
    .pipe(plumber())
        .pipe(gulp.dest(path.prod.img)) // И бросим в build
        .pipe(gulp.dest(path.build.img)) // И бросим в build
        .pipe(reload({stream: true}))

        done()
});


gulp.task('build', gulp.series(
  'html',
  'js',
  'styles',
  // 'fonts',
  'images'
))

gulp.task('watch', gulp.series('build', 'browser-sync', function (done) {
      watch([path.watch.html], function (event, cb) {
        gulp.series('html')
      });
      watch([path.watch.style], function (event, cb) {
        gulp.series('styles')
      });
      watch([path.watch.js], function (event, cb) {
        gulp.series('js')
      })
      watch([path.watch.img], function (event, cb) {
        gulp.series('images')
      })
      // watch([path.watch.fonts], function (event, cb) {
      //   gulp.start('fonts')
      // });
      done()
    })
);
