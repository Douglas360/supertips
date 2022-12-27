import pyodbc
import time
import undetected_chromedriver as uc
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
link_euro = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/span'
link_copa = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/span'
link_premi = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/span'
link_super = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[4]/span'

link_result = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[1]'
link_mostrar_mais = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div'

nm_liga_min_jogo = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/div'
time_casa = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[1]/div'
time_visitante = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[3]/div'

ft_result = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/span '
ht_result = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div[30]/div[2]'
ht_correct_score = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div[31]/div[2]'
ht_correct_score_2 = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[2]/div/div[1]/div[32]/div[2]'


#BetFair
link_liga_clubes_betfair = 'https://www.betfair.com/sport/virtuals/football'
link_liga_copa_betfair = 'https://www.betfair.com/sport/virtuals/football-world-cup'

min_jogo_betfair = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/span[1]'
nm_liga_betfair = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/span[2]'
time_casa_betfair = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]'
time_visitante_betfair = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[3]/div/div[1]/div[1]'

time_casa_ant_betfair = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]'
time_visitante_ant_betfair = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]'

ft_result_casa_betfair = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div'
ft_result_visitante_betfair = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div[3]'

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

        if __name__ == '__main__':
            options = uc.ChromeOptions()

            options.add_argument(
                "--user-data-dir=C:\\Users\\Douglas\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

            self.driver = uc.Chrome(
                options=options
            )

    def raspar_dados(self, liga, id_liga):
        if __name__ == '__main__':
            self.driver.get('https://www.bet365.com/#/AVR/B146/R^1/')

            time.sleep(3)

            try:
                # Clicar no menu da liga

                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, liga))
                )
                element.click()

                time.sleep(1)
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, link_result))
                )
                element.click()

                # Nome da Liga e Minuto de Jogo
                element_nm_liga_min_jogo = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, nm_liga_min_jogo))
                )

                liga = element_nm_liga_min_jogo.text
                liga_minuto = liga.split(" - ")
                self.nm_liga = liga_minuto[0]
                self.min_jogo = liga_minuto[1]

                # Resultado final
                self.element_ft_result = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ft_result))
                )
                result_ft = self.element_ft_result.text

                x = result_ft.split(" - ")

                if len(x) > 1:
                    self.r_time_casa = x[0]
                    self.r_time_fora = x[1]
                else:
                    self.r_time_casa = "undef"
                    self.r_time_fora = "undef"
                # self.export_bd(id_liga)
                # print( self.r_time_casa + " x " +self.r_time_fora )

                # Time da Casa
                self.element_time_casa = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_casa))
                )

                # Time Visitante
                self.element_time_visitante = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_visitante))
                )

                # Clicar em Mostrar Mais
                time.sleep(1)
                element_mostrar_mais = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, link_mostrar_mais))
                )
                element_mostrar_mais.click()

                # Resultado HT
                self.element_ht_result = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ht_result))
                )

                # Resultado Correto HT
                element_ht_correct_score = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, ht_correct_score))
                )

                result_ht = element_ht_correct_score.text

                if result_ht == 'Empate':
                    # Resultado Correto HT
                    element_ht_correct_score = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, ht_correct_score_2))
                    )

                    result_ht = element_ht_correct_score.text

                    x = result_ht.split(" - ")

                    if len(x) > 1:

                        self.correct_score_ht = x[1]
                        y = str(x[1]).split("-")
                        self.correct_score_ht_casa = y[0]
                        self.correct_score_ht_visitante = y[1]
                    else:
                        self.correct_score_ht = "Oth"
                        self.correct_score_ht_casa = "Oth"
                        self.correct_score_ht_visitante = "Oth"

                else:
                    x = result_ht.split(" - ")

                    if len(x) > 1:
                        self.correct_score_ht = x[1]

                        y = str(x[1]).split("-")
                        self.correct_score_ht_casa = y[0]
                        self.correct_score_ht_visitante = y[1]
                    else:
                        self.correct_score_ht = "Oth"
                        self.correct_score_ht_casa = "Oth"
                        self.correct_score_ht_visitante = "Oth"

                self.export_bd(id_liga)

            finally:
                time.sleep(1)

    def raspar_dados_betfair(self, liga):
        if __name__ == '__main__':
            self.driver.get(liga)

            time.sleep(3)

            try:
                # Minuto Jogo
                element_minuto = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, min_jogo_betfair))
                ).text

                x = element_minuto.split(" ")
                self.min_jogo = x[0]

                # Nome Da Liga
                self.nm_liga = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, nm_liga_betfair))
                ).text

                # Time Casa
                self.time_casa = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_casa_betfair))
                ).text

                # Time Visitante
                self.time_visitante = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_visitante_betfair))
                ).text

                # Time Casa Anterior
                self.time_casa_ant = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_casa_ant_betfair))
                ).text

                # Time Visitante Anterior
                self.time_visitante_ant = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_visitante_ant_betfair))
                ).text

                # Resultado Time Casa
                element_result_casa = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ft_result_casa_betfair))
                )
                self.result_casa = element_result_casa.text

                # Resultado Time Visitante
                element_result_visitante = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ft_result_visitante_betfair))
                )
                self.result_visitante = element_result_visitante.text

                self.export_bd_betfair()

            finally:
                time.sleep(1)

    def export_bd_betfair(self):
        comandoInsertLiga = f"""BEGIN TRAN
                        IF NOT EXISTS (select  * from t_liga_betfair where nm_liga = '{self.nm_liga}' )
                        BEGIN
                        insert into  t_liga_betfair (nm_liga)values('{self.nm_liga}') 
                            end
                commit tran"""

        self.cursor.execute(comandoInsertLiga)



        comando = f"""
                       BEGIN TRAN
                       IF NOT EXISTS (select top 1 * from t_jogo_betfair where id_jogo = (SELECT MAX(id_jogo) FROM t_jogo_betfair where id_liga=(select id_liga from t_liga_betfair where nm_liga='{self.nm_liga}'))  and minuto_jogo = '{self.min_jogo}' order by id_jogo desc)
                       BEGIN
                       insert into t_jogo_betfair (
                       id_liga,
                       minuto_jogo,
                       time_casa,
                       time_visitante)
                           values(
                               (select id_liga from t_liga_betfair where nm_liga='{self.nm_liga}'),'{self.min_jogo}','{self.time_casa}','{self.time_visitante}')
                       end
                       commit tran"""

        self.cursor.execute(comando)

        self.cursor.commit()

        comandoUpdate = f"""update t_jogo_betfair set 
                        result_ft_casa='{self.result_casa}',
                        result_ft_visitante= '{self.result_visitante}',
                        dt_atualizacao='{now}'
                        where time_casa=(select top 1 time_casa from t_jogo_betfair where time_casa='{self.time_casa_ant}' order by id_jogo desc) 
                        and time_visitante=(select top 1 time_visitante from t_jogo_betfair where time_visitante='{self.time_visitante_ant}' and dt_atualizacao is null order by id_jogo desc)"""

        self.cursor.execute(comandoUpdate)

        self.cursor.commit()

        print(self.min_jogo + " " + self.nm_liga)
        print(self.time_casa+" x " + self.time_visitante)

        print(self.result_casa + " x " + self.result_visitante)
        print("Finalizou!!")
        print("---------------------")

    def export_bd(self, id_liga):
        comandoInsertLiga = f"""BEGIN TRAN
                IF NOT EXISTS (select  * from t_liga where nm_liga = '{self.nm_liga}' )
                BEGIN
                update t_liga set nm_liga='{self.nm_liga}' where nm_liga like'{self.nm_liga}%'
                end
                commit tran"""

        comandoSelectIDLiga = f"""select id_liga from t_liga where nm_liga='{self.nm_liga}'"""

        self.cursor.execute(comandoInsertLiga)
        self.cursor.execute(comandoSelectIDLiga)

        self.cursor.commit()

        print(self.nm_liga)
        print(self.min_jogo)
        print("Resultado HT: " + self.correct_score_ht_casa + " x " + self.correct_score_ht_visitante)
        print("Resultado FT: " + self.r_time_casa + " x " + self.r_time_fora)

        # print("FT: "+self.element_ft_result.text)
        # print(self.element_time_casa.text + " X "+ self.element_time_visitante.text)
        # print(self.element_time_visitante.text)
        #   print(self.element_ht_result.text)
        # print("HT: "+self.correct_score_ht)

        comando = f"""
                BEGIN TRAN
                IF NOT EXISTS (select top 1 * from t_jogo where id_jogo = (SELECT MAX(id_jogo) FROM t_jogo where id_liga=(select id_liga from t_liga where nm_liga='{self.nm_liga}'))  and minuto_jogo = '{self.min_jogo}' order by id_jogo desc)
                BEGIN
                insert into t_jogo (
                id_liga,
                minuto_jogo,
                time_casa,
                time_visitante,
                result_ft,
                result_ht,
                result_ht_correct_score,
                dt_atualizacao, 
                result_ft_casa,  
                result_ft_visitante, 
                result_ht_correct_score_casa, 
                result_ht_correct_score_visitante)
                    values(
                        (select id_liga from t_liga where nm_liga='{self.nm_liga}'),'{self.min_jogo}','{self.element_time_casa.text}','{self.element_time_visitante.text}','{self.element_ft_result.text}','{self.element_ht_result.text}','{self.correct_score_ht}','{now}','{self.r_time_casa}','{self.r_time_fora}','{self.correct_score_ht_casa}','{self.correct_score_ht_visitante}')
                end
                commit tran"""


        self.cursor.execute(comando)

        self.cursor.commit()

        print("Finalizou!!")
        print("------------")

    pass


connectDB = ConnectDB()



connectDB.raspar_dados_betfair(link_liga_copa_betfair)
connectDB.raspar_dados_betfair(link_liga_clubes_betfair)
