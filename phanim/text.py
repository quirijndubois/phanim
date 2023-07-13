import matplotlib.pyplot as plt
from svgpathtools import svg2paths
import svgpathtools
from lxml import etree
from urllib.parse import urlparse
from .functions import *
import numpy as np
import os

class Tex:

    scale = 1/9600

    def __init__(self,expression,color = (255,255,255),useLatex = True):
        self.filename = f"expression{np.random.randint(0,100)}.svg"
        self.position = [0,0]
        self.color = color
        self.useLatex = useLatex
        self.expression = expression
        self.lineWidth = 1
        self.generate()
    
    def generate(self):
        self.latexToSvg()
        self.getCharacterPositions()
        self.paths, self.attributes = svg2paths(self.filename)
        self.globalOffset = [-self.max/2,0]
        self.refresh()
        os.remove(self.filename)

    def refresh(self):
        self.generateLines()


    def setPosition(self,position):
        self.position = position
        self.refresh()

    def latexToSvg(self):
        fig, ax = plt.subplots()
        self.expression = self.expression.replace(" ","\ ")

        ax.text(0.5, 0.5, f'${self.expression}$', fontsize=16, usetex=self.useLatex)
        ax.axis('off')
        plt.savefig(self.filename, format='svg')
        plt.close(fig)
    
    def getCharacterPositions(self):
        self.max = 0
        tree = etree.parse(self.filename)
        use_elements = tree.xpath('//svg:use', namespaces={'svg': 'http://www.w3.org/2000/svg'})
        transform_values = []

        for use_element in use_elements:
            xlink_href = use_element.get('{http://www.w3.org/1999/xlink}href')
            parsed_href = urlparse(xlink_href)
            id_name = parsed_href.fragment

            transform = use_element.get('transform')
            transform_parts = transform.split(')')

            if 'translate' in transform:
                for part in transform_parts:
                    if part.startswith('translate'):
                        values = part[part.find("(") + 1:].split()
                        values = [float(val) for val in values]
                        transform_values.append([id_name,values])
                        if values[0] > self.max:
                            self.max = values[0]
            else:
                transform_values.append([id_name,[0,0]])



        self.positions = transform_values

    def pathToLines(self,path,offset):
        f = 1/150
        lines = []
        for line in path:
            if type(line) == svgpathtools.path.Line:
                start = line.start
                end = line.end
                startX = start.real*self.scale+offset[0]*f + self.globalOffset[0]*f + self.position[0]
                startY = start.imag*self.scale+offset[1]*f + self.globalOffset[1]*f + self.position[1]
                endX = end.real*self.scale+offset[0]*f + self.globalOffset[0]*f + self.position[0]
                endY = end.imag*self.scale+offset[1]*f + self.globalOffset[1]*f + self.position[1]
                lines.append([
                    [startX, startY],
                    [endX, endY],
                    self.color
                ])
            if type(line) == svgpathtools.path.CubicBezier:
                n = 5
                a = line.start
                b = line.control1
                c = line.control2
                d = line.end
                for i in range(n):
                    t = i/n
                    dt = 1/n
                    start = calculateBezier(a,b,c,d,t)
                    end = calculateBezier(a,b,c,d,t+dt)
                    startX = start.real*self.scale+offset[0]*f + self.globalOffset[0]*f + self.position[0]
                    startY = start.imag*self.scale+offset[1]*f + self.globalOffset[1]*f + self.position[1]
                    endX = end.real*self.scale+offset[0]*f + self.globalOffset[0]*f + self.position[0]
                    endY = end.imag*self.scale+offset[1]*f + self.globalOffset[1]*f + self.position[1]
                    lines.append([
                        [startX, startY],
                        [endX, endY],
                        self.color
                    ])
            
        return lines

    def generateLines(self,completionFactor = 1):
        
        pathDictionary = {}
        namelessPathDictionary = []
        for index,path in enumerate(self.paths):
            try:
                pathDictionary[self.attributes[index]['id']] = path
            except:
                pass
        self.lines = []

        for position in self.positions:
            lines = self.pathToLines(pathDictionary[position[0]],position[1])
            for line in lines:
                self.lines.append(line)
        self.lines = self.lines[:int(len(self.lines)*completionFactor)]

    def createFunction(self,t,old):
        self.generateLines(t)
    