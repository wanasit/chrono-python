import imp
import unittest
import json

enml = imp.load_source('enml', '../enml.py')

class TestENMLOfPlainText(unittest.TestCase):
  
  def setUp(self):
    pass
    
  def test_ENMLOfPlainText(self):
    
    plainText = open('./data_0/ex0.txt', 'r').read()
    enmlText = open('./data_0/ex0.enml', 'r').read()
    enmlText = enmlText.replace("\n","")
    
    createEnml = enml.ENMLOfPlainText(plainText)
    self.assertEqual(createEnml, enmlText)
    
  
    
  def test_PlainTextOfENML(self):

    plainText = open('./data_1/ex1.txt', 'r').read()
    enmlText = open('./data_1/ex1.enml', 'r').read()
    createPlain = enml.PlainTextOfENML(enmlText)

    createPlain = createPlain.strip()
    plainText = plainText.strip()
    self.assertEqual(plainText, createPlain)
  
  
  def test_HTMLOfENML(self):

    htmlText = open('./data_2/ex2.html', 'r').read()
    enmlText = open('./data_2/ex2.enml', 'r').read()
    createHtml = enml.HTMLOfENML(enmlText)
    
    createHtml = createHtml.replace("\n","")
    createHtml = createHtml.strip()
    
    htmlText = htmlText.replace("\n","")
    htmlText = htmlText.strip()
    
    self.assertEqual(htmlText, createHtml)
  
  
  def test_HTMLOfENML_2(self):
  
    shardId = '48' #HARDCODE...
    htmlText = open('./data_3/note3.html', 'r').read()
    jsonText = open('./data_3/note3.json', 'r').read()
    note = json.loads(jsonText)
    
    resources = {}
    for resource in note['resources']:
      
      hash = ''
      for c in resource['data']['bodyHash']:
        if ord(c) < 128 or ord(c) == 65533:
          hash = hash + c
        else:
          hash = hash + (unichr(65533)*2)
      
      resources[hash] = enml.URLOfResource(resource['guid'], shardId)
    
    createHtml = enml.HTMLOfENML(note['content'],resources)
  
    createHtml = createHtml.replace("\n","")
    createHtml = createHtml.strip()
    
    htmlText = htmlText.replace("\n","")
    htmlText = htmlText.strip()
  
    self.assertEqual(htmlText, createHtml)
  


  
if __name__ == '__main__':
    unittest.main()