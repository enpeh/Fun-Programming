# This Python script finds recursively all
# Processing and SuperCollider programs
# under the current directory that have
# been added to Git, then saves the
# resulting list to the file "readme.md",
# which GitHub uses as a read me file.

import os, os.path, subprocess, re

columns = 5

execstr = "git ls-files processing/ideas/ | grep -E '.pde|.scd'"
result = subprocess.check_output(execstr, shell=True).split('\n')

absolutePath = 'https://github.com/hamoid/Fun-Programming/blob/master'

f = open('readme.md', "w")

f.write('''
# Fun Programming

In this repository you can find:

- Programs written for the [Fun Programming](https://funprogramming.org) video
  tutorials: [fun-programming](https://github.com/hamoid/Fun-Programming/tree/master/processing/fun-programming)
- My creative coding experiments: [processing/ideas](https://github.com/hamoid/Fun-Programming/tree/master/processing/ideas).
  These are not finished work but tests I do while developing a project or experiments done just for fun and out of curiosity.
  Index below. You can view some results at https://hamoid.com and at http://hamoid.tumblr.com/archive

Most programs here are written using [Processing](http://www.processing.org/).
Some with [SuperCollider](https://supercollider.github.io/).
They are great for creating static / animated / interactive graphics and sound synthesis.

My current tools include [OPENRNDR](https://openrndr.org) and GLSL.

### Roadmap

- [x] Create thumbnails
- [x] Create a visual index
- [ ] Add tags to each sketch
- [ ] Upload my sketches, one per day. I should be done in 2020.
- [ ] Write a readme.md for each
 
''')
f.write(('| . ' * columns) + '|\n')
f.write(('| --- ' * columns) + '|\n')

col = 0

for line in result:
  if line:
   
    sketchName = os.path.splitext(os.path.basename(line))[0]
    ideaFolder = os.path.dirname(line)
    
    if line.endswith('.pde'):
      if sketchName not in ideaFolder.split('/'):
        continue

    thumb = ""
    if not os.path.exists(ideaFolder + '/.thumb.jpg'):
      if os.path.exists(ideaFolder + '/thumb.png'):
        os.system('imgToSquare.fish %s/thumb.png 150 %s/.thumb.jpg' % (ideaFolder, ideaFolder))
        os.system('git add -f %s/thumb.png' % ideaFolder)
      if os.path.exists(ideaFolder + '/thumb.jpg'):
        os.system('imgToSquare.fish %s/thumb.jpg 150 %s/.thumb.jpg' % (ideaFolder, ideaFolder))
        os.system('git add -f %s/thumb.jpg' % ideaFolder)

    if os.path.exists(ideaFolder + '/.thumb.jpg'):
      t = '%s/.thumb.jpg' % ideaFolder
      thumb = '<br>![](%s)' % t
      if os.popen('git status -s %s' % t).read().startswith('??'):
	      os.system('git add -f %s' % t)
	      print(t)

    sketchName = re.sub("([a-z])([A-Z])","\g<1> \g<2>", sketchName.replace('_', ' '))

    f.write('| [%s%s](%s/%s/) ' % (sketchName, thumb, absolutePath, ideaFolder))
    
    if col % columns == (columns - 1):
      f.write(' |\n')
      
    col = col + 1
    
f.close()

os.system('git add readme.md')

