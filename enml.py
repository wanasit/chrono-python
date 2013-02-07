#!/usr/bin/env python
# -*- coding: utf8 -*-
import re
from xml.etree.ElementTree import XMLParser, Element, SubElement, Comment, tostring

class HTMLCreatorTarget:
  
  root = None
  elements = None
  resources = None
  
  def __init__(self, resources={}):
    self.resources = resources
  
  def start(self, tag, attrib):   # Called for each opening tag.
  
    if tag == 'en-note':
      self.root = Element('html')
      head = SubElement(self.root, 'head')
      meta = SubElement(head,'meta')
      meta.set('http-equiv', 'Content-Type');
      meta.set('content', 'text/html; charset=UTF-8');
      
      body = SubElement(self.root,'body');
      body.set('style', 'word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;');
      self.elements = [self.root, body]
    
    elif tag == 'en-todo':
      todoEle = SubElement(self.elements[-1], 'input', attrib)
      todoEle.set('type', 'checkbox')
      self.elements.append(todoEle)
    
    elif tag == 'en-media':
      
      type = attrib.get('type','')
      hash = attrib.get('hash','')
      width = attrib.get('width',0)
      height = attrib.get('height',0)
      
      if not type.startswith("image") :
        return
      elem = SubElement(self.elements[-1], 'img')
      hash = BodyHashOfENMLHash(hash)
      
      resource = self.resources[hash]
      
      if resource != None:
        elem.set('src', resource)
        
      if width:
        elem.set('width', width)
      if height:
        elem.set('height', height)
      
      self.elements.append(elem)
    
    else :
      self.elements.append( SubElement(self.elements[-1], tag, attrib) )
    
    
  def end(self, tag):             # Called for each closing tag.
    if(tag == 'en-note'):
      pass
    else:
      self.elements.pop()
    
  def data(self, data):
    self.elements[-1].text = data
    
  def close(self):    # Called when all data has been parsed.
    pass
    



def URLOfResource(guid,shardId):
  return 'https://www.evernote.com/shard/'+shardId+'/res/'+guid

def BodyHashOfENMLHash(enmlHash):
  
  buffer = []
  
  for i in range(0, len(enmlHash), 2):
    buffer.append( int(enmlHash[i],16)*16 + int(enmlHash[i+1],16))
  
  bodyHash = ''
  for byte in buffer:
    if byte >= 128 :
      bodyHash += unichr(65533)
    else:
      bodyHash = bodyHash + chr(byte)
  
  return bodyHash
  

def ENMLOfPlainText(text):
  
  lines = re.compile("[\n\r]").split(text)
  
  enml = Element('en-note')
  enml.set('style', 'word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;')
  
  for line in lines:
    block = SubElement(enml, 'div')
    block.text = line
  
  content = '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
  content += tostring(enml,encoding="utf-8",method="xml")
  
  return content


def PlainTextOfENML(text):
  
  try:
    text = re.sub(r'(\r\n|\n|\r)'," ",text)
    text = re.sub(r'(\s+)'," ",text)
    text = re.sub(r'<\/(div|ui|li)>',"\n",text)
    text = re.sub(r'<li>'," - ",text)
    text = re.sub(r'(<([^>]+)>)',"",text)
    
  except (AttributeError, TypeError):
    raise AssertionError('Input variables should be strings')
  
  return text



def HTMLOfENML(text, resources={}):
  
  target = HTMLCreatorTarget(resources)
  parser = XMLParser(target=target)
  parser.feed(text)
  parser.close()
  
  return tostring(target.root, encoding='utf8', method='html')


