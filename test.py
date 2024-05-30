# 导入相关Python库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import hvplot.pandas
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#  忽略警告
warnings.filterwarnings("ignore")


# 读取数据
df = pd.read_csv("../../WA_Fn-UseC_-HR-Employee-Attrition.csv")
# print(df)
# print(df.info())
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文格式,windows
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 年龄
# 年轻员工和年长员工的流失率是否存在差异？
# 不同年龄组的流失模式是否存在基于性别的差异？
# 流失率与年龄的趋势如何？他们之间有关系吗？
age_att=df.groupby(['Age','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
px.line(age_att,x='Age',y='Counts',color='Attrition',title='Age Overview')
# plt.show()
plt.figure(figsize=(8,5))
sns.kdeplot(x=df['Age'],color='MediumVioletRed',shade=True,label='年龄')
plt.axvline(x=df['Age'].mean(),color='k',linestyle ="--",label='平均年龄')
plt.legend()
plt.title('人员流失与年龄的关系')
plt.show()


fig, axes = plt.subplots(1, 2, sharex=True, figsize=(15,5))
fig.suptitle('不同年龄人员流失与性别的关系')
sns.kdeplot(ax=axes[0],x=df[(df['Gender']=='Male')&(df['Attrition']=='Yes')]['Age'], color='r', shade=True, label='Yes')
sns.kdeplot(ax=axes[0],x=df[(df['Gender']=='Male')&(df['Attrition']=='No')]['Age'], color='#01CFFB', shade=True, label='No')
axes[0].set_title('男性')
axes[0].legend(title='是否离职')
sns.kdeplot(ax=axes[1],x=df[(df['Gender']=='Female')&(df['Attrition']=='Yes')]['Age'], color='r', shade=True, label='Yes')
sns.kdeplot(ax=axes[1],x=df[(df['Gender']=='Female')&(df['Attrition']=='No')]['Age'], color='#01CFFB', shade=True, label='No')
axes[1].set_title('女性')
axes[1].legend(title='是否离职')
plt.show()



# 公司男女员工人数比例
att1=df.groupby(['Gender'],as_index=False)['Age'].count()
att1.rename(columns={'Age':'Count'},inplace=True)
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"},{"type": "pie"}]],subplot_titles=('',''))
fig.add_trace(go.Pie(values=att1['Count'],labels=['女性','男性'],hole=0.7,marker_colors=['Red','Blue']),row=1,col=1)
fig.add_layout_image(
    dict(
        source="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8aOWxpkvZGU2EzQ0_USzl6PhuWLi_36xptjeWVXvSqQ2a13MNAjCWyBnhMlkr_ZbFACk&usqp=CAU",
        xref="paper",
        yref="paper",
        x=0.94, y=0.272,
        sizex=0.35, sizey=1,
        xanchor="right", yanchor="bottom", sizing= "contain",
    )
)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.update_layout(title_x=0.5,template='simple_white',showlegend=True,legend_title_text="<b>Gender",title_text='<b style="color:black; font-size:120%;">性别概览',font_family="Times New Roman",title_font_family="Times New Roman")
fig.update_traces(marker=dict(line=dict(color='#000000', width=1.2)))
fig.update_layout(title_x=0.5,legend=dict(orientation='v',yanchor='bottom',y=1.02,xanchor='right',x=1))
fig.add_annotation(x=0.715,
                   y=0.18,
                   text='<b style="font-size:1.2vw" >男性</b><br><br><b style="color:DeepSkyBlue; font-size:2vw">882</b>',
                   showarrow=False,
                   xref="paper",
                   yref="paper",
                  )
fig.add_annotation(x=0.89,
                   y=0.18,
                   text='<b style="font-size:1.2vw" >女性</b><br><br><b style="color:MediumVioletRed; font-size:2vw">588</b>',
                   showarrow=False,
                   xref="paper",
                   yref="paper",
                  )
fig.show()


att1=df.groupby('Attrition',as_index=False)['Age'].count()
att1['Count']=att1['Age']
att1.drop('Age',axis=1,inplace=True)
att2=df.groupby(['Gender','Attrition'],as_index=False)['Age'].count()
att2['Count']=att2['Age']
att2.drop('Age',axis=1,inplace=True)
fig=go.Figure()
fig=make_subplots(rows=1,cols=3)
fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],subplot_titles=('<b>员工流失', '<b>女性流失','<b>男性流失'))
fig.add_trace(go.Pie(values=att1['Count'],labels=att1['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='员工流失',showlegend=False),row=1,col=1)
fig.add_trace(go.Pie(values=att2[(att2['Gender']=='Female')]['Count'],labels=att2[(att2['Gender']=='Female')]['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='女性流失',showlegend=False),row=1,col=2)
fig.add_trace(go.Pie(values=att2[(att2['Gender']=='Male')]['Count'],labels=att2[(att2['Gender']=='Male')]['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='男性流失',showlegend=True),row=1,col=3)
fig.update_layout(title_x=0,template='simple_white',showlegend=True,legend_title_text="<b style=\"font-size:90%;\">Attrition",title_text='<b style="color:black; font-size:120%;"></b>',font_family="Times New Roman",title_font_family="Times New Roman")
fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig.show()


# 婚姻状况
att1=df.groupby('Attrition',as_index=False)['Age'].count()
att1['Count']=att1['Age']
att1.drop('Age',axis=1,inplace=True)
att2=df.groupby(['MaritalStatus','Attrition'],as_index=False)['Age'].count()
att2['Count']=att2['Age']
att2.drop('Age',axis=1,inplace=True)
fig=go.Figure()
fig=make_subplots(rows=1,cols=4)
fig = make_subplots(rows=1, cols=4, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"},{"type": "pie"} ]],subplot_titles=('<b>员工流失' , '<b>结婚流失','<b>单身流失','<b>离婚流失'))
fig.add_trace(go.Pie(values=att1['Count'],labels=att1['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Employee Attrition',showlegend=False),row=1,col=1)
fig.add_trace(go.Pie(values=att2[(att2['MaritalStatus']=='Married')]['Count'],labels=att2[(att2['MaritalStatus']=='Married')]['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Married Attrition',showlegend=False),row=1,col=2)
fig.add_trace(go.Pie(values=att2[(att2['MaritalStatus']=='Single')]['Count'],labels=att2[(att2['MaritalStatus']=='Single')]['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Single Attrition',showlegend=True),row=1,col=3)
fig.add_trace(go.Pie(values=att2[(att2['MaritalStatus']=='Divorced')]['Count'],labels=att2[(att2['MaritalStatus']=='Divorced')]['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Divorced Attrition',showlegend=True),row=1,col=4)
fig.update_layout(title_x=0,template='simple_white',showlegend=True,legend_title_text="<b style=\"font-size:90%;\">Attrition",title_text='<b style="color:black; font-size:120%;"></b>',font_family="Times New Roman",title_font_family="Times New Roman")
fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig.show()



# 收入
rate_att=df.groupby(['MonthlyIncome','Attrition']).apply(lambda x:x['MonthlyIncome'].count()).reset_index(name='Counts')
rate_att['MonthlyIncome']=round(rate_att['MonthlyIncome'],-3)
rate_att=rate_att.groupby(['MonthlyIncome','Attrition']).apply(lambda x:x['MonthlyIncome'].count()).reset_index(name='Counts')
fig=px.line(rate_att,x='MonthlyIncome',y='Counts',color='Attrition',title='按月收入计数员工流失')
fig.show()



#工作部门

dept_att=df.groupby(['Department','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
fig=px.bar(dept_att,x='Department',y='Counts',color='Attrition',title='按工作部门计数员工流失人数')
fig.show()

k=df.groupby(['Department','Attrition'],as_index=False)['Age'].count()
k.rename(columns={'Age':'Count'},inplace=True)
fig=go.Figure()
fig=make_subplots(rows=1,cols=3)
fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],subplot_titles=('人事部', '研发部','销售部'))

fig =fig.add_trace(go.Pie(values=k[k['Department']=='Human Resources']['Count'],labels=k[k['Department']=='Human Resources']['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Human Resources',showlegend=False),row=1,col=1)
fig =fig.add_trace(go.Pie(values=k[k['Department']=='Research & Development']['Count'],labels=k[k['Department']=='Research & Development']['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Research & Development',showlegend=False),row=1,col=2)
fig =fig.add_trace(go.Pie(values=k[k['Department']=='Sales']['Count'],labels=k[k['Department']=='Sales']['Attrition'],hole=0.7,marker_colors=['DeepSkyBlue','LightCoral'],name='Sales',showlegend=True),row=1,col=3)

fig =fig.update_layout(title_x=0.5,template='simple_white',showlegend=True,legend_title_text="Attrition",title_text='<b style="color:black; font-size:100%;">部门员工流失比例',font_family="Times New Roman",title_font_family="Times New Roman")
fig =fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig.show()


#  环境满意度

sats_att=df.groupby(['JobSatisfaction','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
fig = px.area(sats_att,x='JobSatisfaction',y='Counts',color='Attrition',title='基于员工工作满意度计数')
fig.show()


# 工作经验
ncwrd_att=df.groupby(['NumCompaniesWorked','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
fig = px.area(ncwrd_att,x='NumCompaniesWorked',y='Counts',color='Attrition',title='基于员工工作经验计数')
fig.show()




