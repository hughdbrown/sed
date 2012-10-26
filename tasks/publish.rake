# -----------------------------------------------------
# Publish tasks.
# -----------------------------------------------------
namespace "publish" do
  PYTHON_CLIENT_DIR = "client/python/src"
  
  desc "Publish the python client to pynest (requires env var PYNEST)"
  task :python_client do
    vars = %w{ PYNEST }
    check_env_var(vars)
    
    # cd into the correct directory and do the build/deploy
    FileUtils.cd(PYTHON_CLIENT_DIR) do
      cmd = "python setup.py sdist -d #{ENV['PYNEST']}"
      notice(cmd)
      sh(cmd)
    end
  end
end

desc "Publish all code"
task :publish => ["publish:python_client"]
