#from flask import Flask, render_template
#from gabriel import main

#app = Flask(__name__)

#@app.route("/")
#def index():
#    output = main()
#    return render_template("teste.html", output=output)

#if __name__ == "__main__":
#    app.run(debug=True)

from bs4 import BeautifulSoup

with open('teste.html', 'r') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

div_element = soup.find('div', {'id': 'output'})
div_element.string = 'Olá Mundo!'

if div_element is not None:
    div_element.string = 'Olá, mundo!'
else:
    print('Elemento não encontrado.')

# Salva as alterações no arquivo HTML original
with open('original.html', 'w') as f:
    f.write(str(soup))

#if __name__ == "__main__":
#    main()