PROJ = "eLCID"

task :pytest do
  p "Running Python Unit tests for #{PROJ}"
  sh "python manage.py test elcid opal" do | ok, res |
    if not ok # Don't stacktrace please Rake. Ta.
      exit 1
    end
  end
end

task :jstest do
  p "Running Javascript Unit tests for #{PROJ}"
  sh "karma start config/karma.conf.travis.js --browsers Firefox --single-run" do | ok, res |
    if not ok # Don't stacktrace please Rake. Ta.
      exit 1
    end
  end
end

task :devjstest do
  p "Running Javascript Unit tests for #{PROJ}"
  sh "DISPLAY=:10; karma start config/karma.conf.developer.js --browsers Firefox --single-run" do | ok, res |
    if not ok # Don't stacktrace please Rake. Ta.
      exit 1
    end
  end
end

task :test => [:pytest, :jstest] do
  p "Run all tests"
end

task :devtest => [:pytest, :devjstest] do
  p "Run all development tests"
end  
