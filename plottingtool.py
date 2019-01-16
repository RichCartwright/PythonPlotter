try:
    import matplotlib.pyplot as plot
    import csv as csv
    import sys
    import os.path
    from os import path
    import pandas
    from PyInquirer import style_from_dict, Token, prompt, Separator
    from pprint import pprint
except ImportError:
    print('Module Import Error')
    exit()

plotTypes = 'Pie Chart', 'Placeholder1', 'Placeholder2'
dataDir = ''; 
csvData = '';
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def SaveAsPNG(figure):
    plot.savefig('figs/figureTest.png', bbox_inches='tight');

def SetStyle(nStyle = 0):
    stylelist = plot.style.available
    plot.style.use(stylelist[nStyle])

def PlotSelection(selection):
    switch = {  'Pie Chart': PlotPie, 
                'Line Chart': PlotLine,
                'Bar Chart': PlotBar,
                'Scattergraph': PlotScatter
    }
    switch[selection]()

def PlotPie():
    SetStyle(2);
    # TEMP - This needs to hit a data importer    
    labels = 'Python', 'C++', 'Ruby', 'Java'
    values = [212, 130, 245, 210]
    explode = (0.1, 0, 0, 0)
    pieChart = plot.pie(values, explode=explode, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=140);
    print(SaveAsPNG(pieChart))

def PlotLine():
    print("PlotLine() called")

def PlotBar():
    print("PlotBar() called")

def PlotScatter():
    print("PlotScatter() called")

def LoadCSV(dataFile):
    global csvData
    try:
        csvData = pandas.read_csv(dataFile, index_col='country')
    except:
        print('\033[1;31;40m\nSomething messed up reading the CSV file, exiting...')
        exit()


#### ENTRY POINT ####

os.system('clear')
# First check for any arguments that might of been passed in
# Like bash, arg1 is always the script itself so check for 2 or more
if len(sys.argv) >= 2:
    dataDir = sys.argv[1]; 
    if path.exists(dataDir) == False:
        sys.exit("\033[1;31;40m\nData file doesn't exist, exiting...\x1b[0m")
    elif path.isfile(dataDir) == False:
        sys.exit("\033[1;31;40m\nPath not a file, is it a directory? Exiting...\x1b[0m")
    else:
        print("\033[1;35;40m\nData file \"",dataDir,"\" loaded...\x1b[0m")
else:
    dataList = []
    # First we need to find the data file
    for root, dirs, files in os.walk("data/"):
        for fileNames in files:
            if fileNames.endswith(".csv"):
                dataList.append(fileNames)
    
    dataList.sort()

    files = [
            {
                'type': 'list',
                'message': 'Select data to plot',
                'name': 'datacsv',
                'choices': dataList,
                'validate': lambda answer: 'You must choose some data to plot.' \
            }
            ]
    answers = prompt(files, style=style)
    dataDir = dataDir.join(['data/', answers['datacsv']])

#### Main control loop

# First load the CSV in
LoadCSV(dataDir)

while True:
    plotType = [
            {
                'type': 'list',
                'message': 'Select type of plot', 
                'name': 'plot', 
                'choices': [
                    Separator(""),
                    {
                        'name': 'Pie Chart'     
                    },
                    {
                        'name': 'Line Chart'
                    },
                    {
                        'name': 'Bar Chart'
                    },
                    {
                        'name': 'Scattergraph'
                    },
                    ],
                    'validate': lambda answer: 'You must choose a plot type.' \
             }
        ]

    answers = prompt(plotType, style=style)
    PlotSelection(answers['plot']);
    break
