import pyodbc
import time
import undetected_chromedriver as uc
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

link_liga_clubes = 'https://www.betfair.com/sport/virtuals/football'
link_liga_copa = 'https://www.betfair.com/sport/virtuals/football-world-cup'

min_jogo = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/span[1]'
nm_liga = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/span[2]'
time_casa = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]'
time_visitante = '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[3]/div/div[1]/div[1]'

time_casa_ant = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]'
time_visitante_ant = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]'

ft_result_casa = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div'
ft_result_visitante = '/html/body/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div[3]'


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

    def raspar_dados(self, liga):
        if __name__ == '__main__':
            self.driver.get(liga)

            time.sleep(3)

            try:
                # Minuto Jogo
                element_minuto = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, min_jogo))
                ).text

                x = element_minuto.split(" ")
                self.min_jogo = x[0]

                # Nome Da Liga
                self.nm_liga = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, nm_liga))
                ).text

                # Time Casa
                self.time_casa = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_casa))
                ).text

                # Time Visitante
                self.time_visitante = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_visitante))
                ).text

                # Time Casa Anterior
                self.time_casa_ant = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_casa_ant))
                ).text

                # Time Visitante Anterior
                self.time_visitante_ant = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, time_visitante_ant))
                ).text

                # Resultado Time Casa
                element_result_casa = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ft_result_casa))
                )
                self.result_casa = element_result_casa.text

                # Resultado Time Visitante
                element_result_visitante = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ft_result_visitante))
                )
                self.result_visitante = element_result_visitante.text

                self.export_bd()

            finally:
                time.sleep(1)

    def export_bd(self):
        comandoInsertLiga = f"""BEGIN TRAN
                        IF NOT EXISTS (select  * from t_liga_betfair where nm_liga = '{self.nm_liga}' )
                        BEGIN
                        insert into  t_liga_betfair (nm_liga)values('{self.nm_liga}') 
                            end
                commit tran"""

        #comandoSelectIDLiga = f"""select id_liga from t_liga_betfair where nm_liga='{self.nm_liga}'"""

        self.cursor.execute(comandoInsertLiga)
        #self.cursor.execute(comandoSelectIDLiga)

        self.cursor.commit()

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

        #self.cursor.commit()

        comandoUpdate = f"""update t_jogo_betfair set 
                        result_ft_casa='{self.result_casa}',
                        result_ft_visitante= '{self.result_visitante}',
                        dt_atualizacao='{now}'
                        where time_casa=(select top 1 time_casa from t_jogo_betfair where time_casa='{self.time_casa_ant}' order by id_jogo desc) 
                        and time_visitante=(select top 1 time_visitante from t_jogo_betfair where time_visitante='{self.time_visitante_ant}' order by id_jogo desc)"""

        self.cursor.execute(comandoUpdate)

        self.cursor.commit()

        print(self.min_jogo + " " + self.nm_liga)
        print(self.time_casa+" x " + self.time_visitante)

        print(self.result_casa + " x " + self.result_visitante)
        print("Finalizou!!")
        print("---------------------")

    pass


connectDB = ConnectDB()

connectDB.raspar_dados(link_liga_copa)
connectDB.raspar_dados(link_liga_clubes)

