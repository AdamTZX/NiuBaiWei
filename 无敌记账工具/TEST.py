import streamlit as st
import pandas as pd

st.title("狗头线上记账工具（牛百味版）V1.0")
st.subheader("制作者：史上最牛逼的狗头老师")

st.header("")
st.subheader("使用方法介绍")


def display_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
    formatted = text_content.replace('。  ', '。\n\n')

    st.markdown(formatted)


text_path = "文字文档/使用方法介绍.txt"
display_text(text_path)

st.text("备注：侧边页有简易计算器可以辅助进行快速计算")


def calculator():

    with st.sidebar.expander("打开计算器"):
        expression = st.text_input("输入表达式（+：加号，-：减号，*：乘号，/：除号）", "")

        try:
            result = eval(expression)
            st.success(f"结果: {result}")
        except Exception as e:
            st.error(f"计算错误: {e}")


# 运行计算器
calculator()


def accounting_calculator():
    st.title("餐厅收益记账表")

    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=['项目', '金额', '类型'])

    item = st.text_input("项目名称:")
    amount = st.number_input("金额 (¥):", format="%f")
    type_of_entry = st.selectbox("类型", ['收入', '支出'])

    if st.button("添加"):
        new_data = pd.DataFrame({'项目': [item], '金额': [amount], '类型': [type_of_entry]})
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

    st.subheader("删除项")

    selected_item = st.selectbox("选择要删除的项目", st.session_state.data['项目'].unique(), index=0)

    if st.button("删除选定项目"):
        st.session_state.data = st.session_state.data[st.session_state.data['项目'] != selected_item]

    st.subheader("收入表格")
    revenue_data = st.session_state.data[st.session_state.data['类型'] == '收入']
    st.table(revenue_data)

    st.subheader("支出表格")
    expense_data = st.session_state.data[st.session_state.data['类型'] == '支出']
    st.table(expense_data)

    st.subheader("各项利润百分比")
    if not st.session_state.data.empty:
        grouped_data = st.session_state.data.groupby('类型')['金额'].sum()
        total_revenue = grouped_data.get('收入', 0)
        total_expenses = grouped_data.get('支出', 0)

        if total_revenue > 0:
            revenue_percentage = total_revenue / (total_revenue + total_expenses) * 100
            st.write(f"收入利润百分比: {revenue_percentage:.2f}%")

        if total_expenses > 0:
            expenses_percentage = total_expenses / (total_revenue + total_expenses) * 100
            st.write(f"支出利润百分比: {expenses_percentage:.2f}%")

    st.subheader("当日毛利润")
    gross_profit_placeholder = st.empty()

    try:
        gross_profit = total_revenue - total_expenses
        st.write(f"毛利润: {gross_profit:.2f} ¥")
    except Exception as e:
        gross_profit_placeholder.error(f"计算错误: {e}")

    if st.button("导出到Excel"):
        combined_data = pd.concat([revenue_data, expense_data], ignore_index=True)

        combined_data.to_excel("收益记账表.xlsx", index=False)


# 运行记账表应用
accounting_calculator()
