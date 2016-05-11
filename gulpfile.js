var
    gulp = require('gulp'),
    jade = require('gulp-jade'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    changed = require('gulp-changed'),
    imagemin = require('gulp-imagemin'),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    browserify = require('browserify'),
    es = require('event-stream'),
    glob = require('glob'),
    merge = require('merge-stream'),
    bower = require('gulp-bower'),
    sourcemaps = require('gulp-sourcemaps'),
    livereload = require('gulp-livereload'),
    exec = require('child_process').exec;

var config = {
    assets: './assets/',
     bowerDir: './bower_components' ,
    templates: './databeesProject/databeesProject/templates/',
    static : './databeesProject/databeesProject/static/',
}

gulp.task('jade', function() {
    return gulp.src([config.assets + 'templates/**/*.jade', '!' + config.assets + 'templates/template/**/_*.jade'])
        .pipe(jade({
            pretty: true
        }))
        .on('error', console.log)
        .pipe(gulp.dest(config.templates))
        .pipe(livereload());
});

gulp.task('email-txt-tamplates', function() {
    return gulp.src([config.assets + 'templates/email/*.txt'])
        .on('error', console.log)
        .pipe(gulp.dest(config.templates + 'email/'))
        .pipe(livereload());
});

gulp.task('sass', function() {
    
    return gulp.src([config.assets + 'sass/**/*.scss', '!' + config.assets + 'sass/**/_*.scss'])
    .pipe(sourcemaps.init())
    .pipe(sass({
        outputStyle: 'compressed',
        includePaths: [
            './resources/sass',
            config.bowerDir + '/foundation/scss',
            config.bowerDir + '/animate-sass',
            config.bowerDir + '/font-awesome/scss',
            config.assets + 'sass/includes']
        }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(config.static + 'css/'))
    .pipe(livereload());
});


gulp.task('fonts', function() {
    return gulp.src(config.assets + 'fonts/**/*')
    .pipe(gulp.dest(config.static + 'fonts/'));
});

gulp.task('icons', function() { 
    return gulp.src(config.bowerDir + '/font-awesome/fonts/**.*') 
        .pipe(gulp.dest(config.static + 'fonts/')); 
});

gulp.task('browserify', function(done) {
    glob(config.assets + 'js/**.js', function(err, files) {
        if (err) done(err);

        var tasks = files.map(function(entry) {
            return browserify({
                    entries: [entry]
                })
                .bundle()
                .pipe(source(entry))
                .pipe(rename({
                    dirname: "",
                    extname: '.bundle.js'
                }))
                .pipe(buffer())
                .pipe(sourcemaps.init({loadMaps: true}))
                .pipe(uglify())
                .pipe(sourcemaps.write('./'))
                .pipe(gulp.dest(config.static + 'js/'));
        });
        es.merge(tasks).on('end', done).pipe(livereload());;
    });
});

gulp.task('images', function() {
    return gulp.src(config.assets + 'images/**/*')
        .pipe(imagemin())
        .pipe(gulp.dest(config.static + 'images/'))
        .pipe(livereload());;
});


gulp.task('bower_components', function() {
    return gulp.src(bowerFiles())
        .pipe(filter('**/*.css'))
        .pipe(gulp.dest('./assets/css'));
});

gulp.task('bower', function() { 
    return bower()
         .pipe(gulp.dest(config.bowerDir)) 
});

gulp.task('collectstatic', function() {
    var isWin = /^win/.test(process.platform);
    var cmd =  "bash -l -c 'workon databeesProject && PYTHONUNBUFFERED=1 python ./databeesProject/manage.py collectstatic --noinput'";
    var proc = exec(cmd);
    proc.stderr.on('data', function(data) {
      process.stdout.write(data);
    });

    proc.stdout.on('data', function(data) {
      process.stdout.write(data);
    });
});

gulp.task('default', ['bower', 'jade', 'email-txt-tamplates', 'sass', 'images', 'browserify', 'icons', 'fonts', 'collectstatic'], function() {
    livereload.listen();
    gulp.watch(config.assets + 'sass/**/*.scss', ['sass', 'collectstatic']);
    gulp.watch(config.assets + 'templates/**/*.jade', ['jade', 'collectstatic']);
    gulp.watch(config.assets + 'templates/email/*.txt', ['email-txt-tamplates', 'collectstatic']);
    gulp.watch(config.assets + 'images/**/*', ['images', 'collectstatic']);
    gulp.watch(config.assets + 'js/**/*', ['browserify', 'collectstatic']);
});