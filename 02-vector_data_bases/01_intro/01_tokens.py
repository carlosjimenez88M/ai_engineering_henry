#!/usr/bin/env python
"""
01_tokens.py

Objetivo del script: 
Script description goes here.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# coding: utf-8

# ![Henry Logo](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)
# 
# # Introducción a las bases de datos vectoriales 
# ## Clase #1 : Tokens y representación de las palabras
# 

# In[1]:


from transformers import AutoTokenizer
import tiktoken
import warnings
warnings.filterwarnings('ignore')


# In[2]:


### Auxiliary functions
colors = [
    '102;194;165', '252;141;98', '141;160;203',
    '231;138;195', '166;216;84', '255;217;47'
]
def show_tokens(sentence: str, tokenizer_name: str):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    token_ids = tokenizer(sentence).input_ids


    print(f"Vocab length: {len(tokenizer)}")

    # Print a colored list of tokens
    for idx, t in enumerate(token_ids):
        print(
            f'\x1b[0;30;48;2;{colors[idx % len(colors)]}m' +
            tokenizer.decode(t) +
            '\x1b[0m',
            end=' '
        )


# In[3]:


sentence = """Dale a tu cuerpo alegría, Macarena
Que tu cuerpo es pa' darle alegría y cosa buena
Dale a tu cuerpo alegría, Macarena
Eh, Macarena (¡ay!)

Dale a tu cuerpo alegría, Macarena
Que tu cuerpo es pa' darle alegría y cosa buena
Dale a tu cuerpo alegría, Macarena
Eh, Macarena (¡ay!)

Macarena tiene un novio que se llama
Que se llama de apellido Vitorino
Que en la jura de bandera del muchacho
Se la dio con dos amigos (¡ay!)
"""


# In[4]:


# Tokens con Bert
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
token_ids = tokenizer(sentence).input_ids
print(token_ids)
print(len(token_ids))


# In[5]:


for id in token_ids:
    print(tokenizer.decode(id))


# In[6]:


colors = [
    '102;194;165', '252;141;98', '141;160;203',
    '231;138;195', '166;216;84', '255;217;47'
]


# In[7]:


show_tokens(sentence, "bert-base-cased")


# ### Cambiando al modelo de OpenAI

# In[8]:


encoder = tiktoken.encoding_for_model("gpt-4o")
tokens = encoder.encode(sentence)
print(f"Tokens: {tokens}")
print(f"Cantidad de tokens: {len(tokens)}")


# In[12]:


for id in tokens:
    print(id)


# In[18]:


for id in tokens:
    words = encoder.decode([id])
    print(words.strip())

