# Builds the site by calling Jekyll's Ruby API directly.
#
# Why not just `jekyll build`? The `jekyll` command-line stub insists on em-websocket,
# which it only needs for `jekyll serve`, and that gem's native extension will not compile
# against the Ruby 2.6 that macOS ships. Calling the API skips that dependency.
#
# Run it through bin/preview.sh — not directly.

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

require 'jekyll'

dest = ENV['SITE'] or abort 'SITE env var not set'

config = Jekyll.configuration(
  'source'      => Dir.pwd,
  'destination' => dest,
  'quiet'       => true
)

begin
  Jekyll::Site.new(config).process
  puts "built #{Dir.glob(File.join(dest, '*.html')).size} pages -> #{dest}"
rescue => e
  warn "BUILD FAILED: #{e.class}: #{e.message}"
  warn e.backtrace.first(6).map { |l| "  #{l}" }.join("\n")
  exit 1
end
