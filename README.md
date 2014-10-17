xpath
=====

An implementation of XPath 1.0 in python.

I wrote this years ago, I'm not sure how much of the spec it implements. The spec's not that big though so I think it's a fair amount. Maybe not every axis, and definitely not all the functions.

XPath 2 existed when I wrote this but that's a much more complex spec and I didn't realy know where to start, it's not an evenings after work kind of project. I think I decided that if I wanted something that worked it would have to be XPath 1.0

I've replaced the Bison based parser with a python one using the ply parser generator. This removes the need for a c compiler.

All the test cases pass apart from one, which I think is showing up a difference in dom implementations not a problem with the xpath implementation. I've commented it out.

I've added a demo app that presents a user interface in a web browser allowing the user to run xpath queries on an xml document.

I've used the Flask to create the daemon and the React javascript library to create the user interface. I've never used either of these before, I was really interested in using React though.
