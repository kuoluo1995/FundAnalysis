import subprocess
from matplotlib.font_manager import FontManager

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)
output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
zh_fonts = set(f.split(',', 1)[0] for f in output.decode('utf-8').split('\n'))
available = mat_fonts & zh_fonts
print ('*' * 10, '可用的字体', '*' * 10)
for f in available:
     print (f)