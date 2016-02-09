SnippetX
============

## Turn tabular data into code!

SnippetX takes comma-seperated data (csv) and combines it with a snippet of your choosing. It's like xarg but for snippets.

## Demo

![SnippetX](example/example.gif)

## Installation

Download it using Package Control.

## Usage

Place comma-seperated values in your view or open a csv file. At the bottom or top add 'sx:' followed by the tabTrigger of the snippet you'd like to use. Make sure there are newlines between the data you want manipulated and anything else. Hit Alt+x. Each line will replaced with the snippet you chose, with the data from the line placed in the snippet. 

Where the data ends up depends on it's column number and sublime placeholder. IE, anything in column one maps to placeholder $1. You can use the placeholders out of order or multiple times and you can give them default values, in the event that your data has missing fields. If there are more placeholders than columns then the last few placeholders will be either empty or default values. If there are more columns than placeholders than SnippetX will use only as many as columns as there are placeholders (Note that the full line would still be replaced).

Also note that any regular sublime snippet can be used. Nothing special has to be added to make this work. The snippets you use everyday work fine with SnippetX.

## License

MIT © [Colin Ryan](http://github.com/ColinRyan)