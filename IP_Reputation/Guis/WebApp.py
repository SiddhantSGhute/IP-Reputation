import sys

import pandas as pd
from Scripts.Mail import SendMail
sys.path.append(r"E:\OptiveProject")
import streamlit as st
from Guis.Perform import Processor


def close():
    st.session_state.checkbox1 = False
    st.session_state.load_back = False

processor = Processor()
st.title("IP-Reputation")

placeholder = st.empty()
placeholder.subheader("Abuse & Virus Limit : 1000 / 500")
st.markdown('---')

options = ['Single','Multiple','File']
choices = st.radio("Select Type : ", options= options,horizontal= True)
if choices == options[0]:
    value = "Please Enter Single IP : "
    ip_input,btn = st.columns([8,1])

    with ip_input:
        ip = st.text_input(value)
        ip = processor.check_single_ip(ip)
        processor.ipaddress = [ip]
    with btn:
        st.write("#")
        btn1 = st.button("Submit")
        if "load_back" not in st.session_state:
            st.session_state['load_back'] = False


    if btn1 or st.session_state.load_back:
        st.session_state.load_back = True

        if not ip:
            st.warning("You Have Entered The Invalid IP Address")
        else:
            processor.processIP()
            abuse_data = processor.metadata['AbuseIP_Data']
            abuse_data['IP'] = abuse_data['Data']['ipAddress']
            virus_data = processor.metadata['VirusTotal_Data']

            raw , table = st.columns(2)
            with raw:
                with st.expander('Abuse Raw Data'):
                    st.json(abuse_data)
                if virus_data:
                    with st.expander('VirusTotal Raw Data'):
                        st.json(virus_data)

            # show Table Format
            with table:

                with st.expander('Abuse Table Data'):
                    abuse_df = pd.DataFrame([abuse_data['Data']])
                    try:
                        abuse_df = abuse_df.drop(['_id'],axis= "columns")
                    except:
                        pass
                    # st.write(abuse_df)
                    st.dataframe(abuse_df)
                if virus_data:
                    with st.expander('VirusTotal Table Data'):
                        virus_df = pd.DataFrame([virus_data['Data']])
                        try:
                            virus_df = virus_df.drop(['_id'],axis= "columns")
                        except:
                            pass
                        st.dataframe(virus_df)
            checkbox1 = st.checkbox("Save & Email")
            if checkbox1 not in st.session_state:
                st.session_state.checkbox1 = False


            if checkbox1 or st.session_state.checkbox1:
                st.session_state.checkbox1 = True
                emails = st.text_input("Enter Single/Multiple Comma Separated Email Ids : ").strip().split(',')
                placeholder2 = st.empty()
                btn2 = placeholder2.button("Submit",key="1")
                if btn2:
                    try:
                        btn2 = placeholder2.button("Submit",key=2,disabled= True)
                        processor.saveAbuse()
                        processor.createHtml()
                        SendMail(f"{processor.html}",emails,[processor.abuse_filename,processor.virus_filename])
                        processor.reset()
                        st.success("Mail Has Been Sent")
                        close()
                    except Exception as e:
                        st.error(e)


elif choices == options[1]:
    close()
    all_abuse_data = []
    all_virus_data = []
    value = "Please Enter Multiple IPs Comma Separated"
    ip_input, btn = st.columns([8, 1])

    with ip_input:
        ip = st.text_input(value).strip().split(',')
        ip = [i.strip() for i in ip]
        ips = []
        for i in ip:
            if processor.check_single_ip(i):
                ips.append(i)

        processor.ipaddress = ips
        processor.processIP()


    with btn:
        st.write("#")
        btn1 = st.button("Submit")
        if "load_back_1" not in st.session_state:
            st.session_state['load_back_1'] = False

    if btn1 or st.session_state.load_back_1:
        st.session_state.load_back_1 = True

        if not ip:
            st.warning("You Have Entered The Invalid IP Address")
        else:

            abuse_data = processor.AbuseData
            virus_data = processor.VirusData

            raw, table = st.columns(2)
            with raw:
                with st.expander('Abuse Raw Data'):
                    st.json(abuse_data)
                if virus_data:
                    with st.expander('VirusTotal Raw Data'):
                        st.json(virus_data)

            # show Table Format
            with table:

                with st.expander('Abuse Table Data'):
                    abuse_df = pd.DataFrame(abuse_data)
                    try:
                        abuse_df = abuse_df.drop(['_id'], axis="columns")
                    except:
                        pass
                    # st.write(abuse_df)
                    st.dataframe(abuse_df)
                if virus_data:
                    with st.expander('VirusTotal Table Data'):
                        virus_df = pd.DataFrame(virus_data)
                        try:
                            virus_df = virus_df.drop(['_id'], axis="columns")
                        except:
                            pass
                        st.dataframe(virus_df)
            checkbox2 = st.checkbox("Save & Email")
            if checkbox2 not in st.session_state:
                st.session_state.checkbox2 = False

            if checkbox2 or st.session_state.checkbox2:
                st.session_state.checkbox2 = True
                emails = st.text_input("Enter Single/Multiple Comma Separated Email Ids : ").strip().split(',')
                placeholder2 = st.empty()
                btn2 = placeholder2.button("Submit", key="1")
                if btn2:
                    try:
                        btn2 = placeholder2.button("Submit", key=2, disabled=True)
                        processor.saveAbuse()
                        processor.createHtml()
                        SendMail(f"{processor.html}",emails,[processor.abuse_filename,processor.virus_filename])
                        processor.reset()
                        st.success("Mail Has Been Sent")
                        close()
                    except Exception as e:
                        st.error(e)


else:
    header = st.text_input("Please Enter The Column name : ")
    uploaded_file = st.file_uploader("please Upload a file that contains IPs : ", type= ["csv"])





"st.session object after : ",st.session_state
#
# for key in st.session_state.keys():
#     del st.session_state[key]