import pyodbc
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


#now = '2022 - 10 - 14 13:24:53.990'
link_result = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[1]'
link_mostrar_mais = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div'

nm_liga_min_jogo = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/div'
time_casa = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[1]/div'
time_visitante = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[3]/div'

ft_result = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/span '
ht_result = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div[30]/div[2]'
ht_correct_score = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div[31]/div[2]'


class ConnectDB:

    def __init__(self):
        self.cursor = None
        self.create_connection()


    def create_connection(self):
        self.dados_conexao = (
            "Driver={SQL Server};"
            "Server=xbigdata.cvvtqgy2croi.us-east-1.rds.amazonaws.com;"
            "UID=sa;"
            "PWD=Suporte*13;"
            "Database=bet365-api;"
        )

        self.conexao = pyodbc.connect(self.dados_conexao)
        self.cursor = self.conexao.cursor()


    def export_bd(self):

        comando = f"""insert into t_jogo (id_liga,minuto_jogo,time_casa,time_fora,result_ft,result_ht,result_ht_correct_score,dt_atualizacao)
                      values
                      (1,'19.35','Turquia','França','0 - 2','Empate','0-0','{now}')"""
        self.cursor.execute(comando)
        self.cursor.commit()
        self.cursor.close()
        self.conexao.close()

        print("Finalizou!!")
        print(now)
    pass


connectDB = ConnectDB()
connectDB.export_bd()
