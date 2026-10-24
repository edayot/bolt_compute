
using storage example:main foo as foo
using storage example:main bar.baz as bar
using storage example:main bill as baz

# data modify foo.1 set value 1
# data modify foo.2 set value 2

compute default float baz["ty"]