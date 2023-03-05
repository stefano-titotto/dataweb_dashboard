#!/usr/bin/env python
# coding: utf-8

# # US Quartz Import Dashboard
# 
# Mi ha ispirato il video:https://youtu.be/uhxiXOTKzfs di Thu Vu
# 

# ## Impostazione strutture dati

# In[1]:


import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator') #

import hvplot.pandas


# In[2]:


df = pd.read_csv('dataweb.csv', delimiter=';',na_filter=True)
#df.info()


# In[3]:


# elimina i rughe nulle
df.dropna(inplace=True)
#df.head()


# In[4]:


# sostituisci la , con il . e converti in float
df['value'] = df['value'].str.replace(',', '.').astype(float)


# In[5]:


#df.head()


# In[6]:


# Elimina i valori usd/sqm e le righe con valore 0
df = df[(df['Unit']!='usd/sqm') & (df['value']!= 0)]


# In[7]:


tab = pd.pivot_table(df, values=["value"], index=["Year", "Country"], columns= ["Unit"], aggfunc=np.sum)
#tab


# ## Pannelli interattivi

# In[8]:


idf = df.interactive()


# In[9]:


# Definisci i widgets
year_slider = pn.widgets.IntSlider(name='Year slider', start=2015, end=2022, step=1, value = 2021)
#year_slider 


# In[11]:


y_axis = pn.widgets.RadioButtonGroup(
    name='Unit',
    options=['sqm', 'usd',],
    button_type='success'
)
#y_axis


# In[12]:


import_pipeline = (
    idf[
        (idf['Year']==year_slider)&
        (idf['Unit']==y_axis)
    ]
    .groupby(['Country']).sum().filter(items=['Country', 'value'])
    .sort_values(by='value', ascending=False)
    .head(10)
)


# In[13]:


#import_pipeline


# In[15]:


import_plot = import_pipeline.hvplot(x='Country', kind='bar', title="Major quartz exporters to USA")
#import_plot


# ## Pubblica il pannello

# In[19]:


#Layout using Template
template = pn.template.FastListTemplate(
    title='US import statistics for quartz slabs', 
    sidebar=[pn.pane.Markdown("# Top Ten in the years"), 
             pn.pane.Markdown("#### See how in the years the portfolio of countries supplying slabs changed."),
             # pn.pane.PNG('climate_day.png', sizing_mode='scale_both'),
             pn.pane.Markdown("## Settings"),
            ],
    main=[pn.Column(import_plot.panel(width=700), y_axis,year_slider, margin=(0,25)),
         ],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
# template.show()
template.servable();


# ** Istruzioni **
# 
# per far partire il server dalla console:
# 
# >  panel serve USImport_dashboard.ipynb

# In[ ]:
