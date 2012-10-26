# -----------------------------------------------------
# Lint tasks.
# -----------------------------------------------------
namespace "test" do

  desc "Run the pylint analysis tool."
  task :unit => ["setup:test"] do
    FileUtils.cd(File.join(CLIENT_TEST_DIR, "unit")) do
      cmd = "nosetests #{Dir.pwd}"
      notice(cmd)
      sh(cmd)
    end
  end

  desc "Run the pep8 analysis tool."
  task :integration => ["setup:test"] do
    FileUtils.cd(File.join(CLIENT_TEST_DIR, "integration")) do
      cmd = "nosetests #{Dir.pwd}"
      notice(cmd)
      sh(cmd)
    end
  end
end

desc "Run all code analysis tools."
task :test => ["test:unit", "test:integration"]
