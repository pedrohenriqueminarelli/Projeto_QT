import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QDialog,
                               QMessageBox, QTableWidgetItem, QInputDialog)
from PySide6.QtCore import QDate
from FrmEmpregado_ui import Ui_FrmEmpregado
from FrmConexao_ui import Ui_dlgConexao
import pyodbc as bd
from datetime import datetime, date


class DialogoConexao(QDialog, Ui_dlgConexao):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)


class FormPrincipal(QMainWindow, Ui_FrmEmpregado):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mensagem = QStatusBar()
        self.setStatusBar(self.mensagem)

        self.acao_Sair.triggered.connect(self.sair_do_programa)
        self.acao_Novo.triggered.connect(self.novo_registro)
        self.acao_Editar.triggered.connect(self.editar_registro)
        self.acao_Salvar.triggered.connect(self.salvar_registro)
        self.acao_Excluir.triggered.connect(self.excluir_registro)
        self.acao_Cancelar.triggered.connect(self.cancelar_acao)
        self.acao_Buscar.triggered.connect(self.buscar_registro)
        self.abas.currentChanged.connect(self.mudar_aba)

        self.acao_Inicio.triggered.connect(self.ir_ao_inicio)
        self.acao_Anterior.triggered.connect(self.ir_ao_anterior)
        self.acao_Proximo.triggered.connect(self.ir_ao_proximo)
        self.acao_Fim.triggered.connect(self.ir_ao_fim)

        self.dados = []           
        self.quantos_dados = 0    
        self.registro_atual = -1  

        self.cbSexo.clear()
        self.cbSexo.addItems(["M", "F"])

        self.preencher_combo_deptos()  
        self.buscar_dados()            
        self.atualizar_tela()         
        
        self.edCpf.setReadOnly(True)

        self.show()

        
        self.modo_do_programa = "navegando"

    
    def preencher_combo_deptos(self):
        try:
            comando = "SELECT NumDepto, NomeDepto FROM V_Emp.Departamento " +\
                      " ORDER BY NomeDepto"
            resultado = meu_cursor.execute(comando)
            self.cbDepto.clear()
            
            self.cbDepto.addItem("(sem departamento)", None)
            for depto in resultado.fetchall():
                self.cbDepto.addItem(depto[1], depto[0])
        except Exception as erro:
            self.mensagem.showMessage("Erro ao buscar departamentos: " + str(erro))

    def buscar_dados(self):
        try:
            comando = "SELECT cpf, PreNome, InicialMeio, Sobrenome, dataNascimento, " +\
                      " Endereco, Sexo, Salario, NumDepto, super_cpf " +\
                      " FROM V_Emp.Empregado " +\
                      " ORDER BY PreNome, Sobrenome"
            resultado = meu_cursor.execute(comando)
            self.dados = resultado.fetchall()     
            self.quantos_dados = len(self.dados) 
            if self.quantos_dados > 0:
                self.registro_atual = 0          
            else:
                self.registro_atual = -1
        except Exception as erro:
            print("Erro ao buscar os dados para navegação:", erro)

    def ir_ao_inicio(self):
        if self.quantos_dados > 0:
            self.registro_atual = 0
            self.atualizar_tela()

    def ir_ao_anterior(self):
        if self.registro_atual > 0:
            self.registro_atual -= 1    
            self.atualizar_tela()

    def ir_ao_proximo(self):
        if self.registro_atual < self.quantos_dados - 1:
            self.registro_atual += 1    
            self.atualizar_tela()

    def ir_ao_fim(self):
        if self.quantos_dados > 0:
            self.registro_atual = self.quantos_dados - 1
            self.atualizar_tela()

 
    def para_qdate(self, valor):
        if valor is None:
            return QDate.currentDate()
        if isinstance(valor, str):
            valor = datetime.strptime(valor[:10], '%Y-%m-%d')
        return QDate(valor.year, valor.month, valor.day)

    def atualizar_tela(self):
        if self.quantos_dados > 0:  
            emp = self.dados[self.registro_atual]
            self.edCpf.setText(emp[0])
            self.edPreNome.setText(emp[1] or "")
            self.edInicialMeio.setText(emp[2] or "")
            self.edSobrenome.setText(emp[3] or "")
            self.deDataNasc.setDate(self.para_qdate(emp[4]))
            self.edEndereco.setText(emp[5] or "")
            self.cbSexo.setCurrentIndex(self.cbSexo.findText(emp[6] or ""))
            self.dsbSalario.setValue(float(emp[7] or 0))
            
            posicao = self.cbDepto.findData(emp[8])
            if posicao < 0:
                posicao = 0     
            self.cbDepto.setCurrentIndex(posicao)
            self.edSupervisorCpf.setText(emp[9] or "")
            self.mensagem.showMessage(
                f"Registro {self.registro_atual + 1}/{self.quantos_dados}")
        else:
            self.limpar_tela() 

    def limpar_tela(self):
        self.edCpf.setText("")
        self.edPreNome.setText("")
        self.edInicialMeio.setText("")
        self.edSobrenome.setText("")
        self.deDataNasc.setDate(QDate.currentDate())
        self.edEndereco.setText("")
        self.cbSexo.setCurrentIndex(0)
        self.dsbSalario.setValue(0)
        self.cbDepto.setCurrentIndex(0)
        self.edSupervisorCpf.setText("")

    def sair_do_programa(self):
        self.close()

   
    def novo_registro(self):
        self.modo_do_programa = "incluindo"
        self.limpar_tela()
        self.edCpf.setReadOnly(False)   
        self.edCpf.setFocus()
        self.mensagem.showMessage("Inclusão: digite os dados acima")

    
    def editar_registro(self):
        if self.quantos_dados == 0:
            self.mensagem.showMessage("Não há empregado para editar.")
            return
        self.modo_do_programa = "editando"
        self.edCpf.setReadOnly(True)    
        self.edPreNome.setFocus()
        self.mensagem.showMessage("Edição: altere os dados acima")

    
    def salvar_registro(self):
        if self.modo_do_programa == "incluindo":
            self.realizar_insert()
        elif self.modo_do_programa == "editando":
            self.realizar_update()
        else:
            self.mensagem.showMessage("Antes de salvar, clique em [Novo] ou em [Editar].")

   
    def texto_ou_nulo(self, texto):
        texto = texto.strip()
        return texto if texto != "" else None

   
    def dados_validos(self):
        if self.edCpf.text().strip() == "":
            QMessageBox.warning(self, "Atenção", "Digite o CPF do empregado.")
            self.edCpf.setFocus()
            return False
        if self.edPreNome.text().strip() == "" or self.edSobrenome.text().strip() == "":
            QMessageBox.warning(self, "Atenção", "Digite o prenome e o sobrenome.")
            self.edPreNome.setFocus()
            return False
        if self.edSupervisorCpf.text().strip() == self.edCpf.text().strip():
            QMessageBox.warning(self, "Atenção",
                                "O empregado não pode ser supervisor de si mesmo.")
            self.edSupervisorCpf.setFocus()
            return False
        return True

    
    def recarregar_e_posicionar(self, cpf):
        self.buscar_dados()
        for indice in range(self.quantos_dados):
            if self.dados[indice][0].strip() == cpf.strip():
                self.registro_atual = indice
                break
        self.atualizar_tela()

    def voltar_a_navegar(self):
        self.modo_do_programa = "navegando"
        self.edCpf.setReadOnly(True)

    def realizar_insert(self):
        if not self.dados_validos():
            return
        comando = "INSERT INTO V_Emp.Empregado " +\
                  " (cpf, PreNome, InicialMeio, Sobrenome, dataNascimento, " +\
                  "  Endereco, Sexo, Salario, NumDepto, super_cpf) " +\
                  " VALUES (?, ?, ?, ?, Convert(date, ?, 103), ?, ?, ?, ?, ?)"
        cpf = self.edCpf.text().strip()
        try:
            meu_cursor.execute(comando,
                               cpf,
                               self.edPreNome.text().strip(),
                               self.texto_ou_nulo(self.edInicialMeio.text()),
                               self.edSobrenome.text().strip(),
                               self.deDataNasc.date().toString('dd/MM/yyyy'),
                               self.texto_ou_nulo(self.edEndereco.text()),
                               self.cbSexo.currentText(),
                               self.dsbSalario.value(),
                               self.cbDepto.currentData(),   
                               self.texto_ou_nulo(self.edSupervisorCpf.text()))
            meu_cursor.commit()  
            self.voltar_a_navegar()
            self.recarregar_e_posicionar(cpf)
            self.mensagem.showMessage("Novo empregado foi inserido.")
        except bd.IntegrityError as erro:  
            meu_cursor.rollback()
            texto = str(erro)
            if "PRIMARY KEY" in texto.upper() or "duplicate" in texto.lower():
                motivo = "Já existe um empregado com esse CPF."
            elif "FOREIGN KEY" in texto.upper():
                motivo = "O CPF do supervisor não existe na tabela de empregados."
            else:
                motivo = "Os dados violam uma regra do banco de dados."
            QMessageBox.warning(self, "Não foi possível incluir", motivo +
                                "\n\nDetalhe técnico:\n" + texto)
        except Exception as erro: 
            meu_cursor.rollback()
            QMessageBox.warning(self, "Erro ao incluir", str(erro))

    def realizar_update(self):
        if not self.dados_validos():
            return
        comando = "UPDATE V_Emp.Empregado " +\
                  " SET PreNome = ?, InicialMeio = ?, Sobrenome = ?, " +\
                  "     dataNascimento = Convert(date, ?, 103), Endereco = ?, " +\
                  "     Sexo = ?, Salario = ?, NumDepto = ?, super_cpf = ? " +\
                  " WHERE cpf = ?"
        cpf = self.edCpf.text().strip()
        try:
            meu_cursor.execute(comando,
                               self.edPreNome.text().strip(),
                               self.texto_ou_nulo(self.edInicialMeio.text()),
                               self.edSobrenome.text().strip(),
                               self.deDataNasc.date().toString('dd/MM/yyyy'),
                               self.texto_ou_nulo(self.edEndereco.text()),
                               self.cbSexo.currentText(),
                               self.dsbSalario.value(),
                               self.cbDepto.currentData(),
                               self.texto_ou_nulo(self.edSupervisorCpf.text()),
                               cpf)
            meu_cursor.commit()
            self.voltar_a_navegar()
            self.recarregar_e_posicionar(cpf)
            self.mensagem.showMessage("Registro alterado.")
        except bd.IntegrityError as erro:
            meu_cursor.rollback()
            QMessageBox.warning(self, "Não foi possível alterar",
                                "O CPF do supervisor ou o departamento informado não existe."
                                "\n\nDetalhe técnico:\n" + str(erro))
        except Exception as erro:
            meu_cursor.rollback()
            QMessageBox.warning(self, "Erro ao alterar", str(erro))

    def excluir_registro(self):
        if self.quantos_dados == 0:
            self.mensagem.showMessage("Não há empregado para excluir.")
            return
        self.modo_do_programa = "excluindo"
        nome = self.edPreNome.text() + " " + self.edSobrenome.text()
        resposta = QMessageBox.question(
            self,
            "Confirmação de Exclusão",
            f"Tem certeza de que deseja excluir o empregado {nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            self.realizar_delete()
        else:
            self.mensagem.showMessage("Empregado foi mantido.")
        self.modo_do_programa = "navegando"

    def realizar_delete(self):
        comando = "DELETE FROM V_Emp.Empregado WHERE cpf = ?"
        try:
            meu_cursor.execute(comando, self.edCpf.text().strip())
            meu_cursor.commit()

            self.dados.pop(self.registro_atual)
            self.quantos_dados -= 1
            if self.registro_atual >= self.quantos_dados:
                self.registro_atual = self.quantos_dados - 1
            self.atualizar_tela()
            self.mensagem.showMessage("Empregado excluído.")
        except bd.IntegrityError as erro:  
            meu_cursor.rollback()
            QMessageBox.warning(
                self, "Não foi possível excluir",
                "Este empregado está ligado a outros registros do banco e não pode ser excluído.\n"
                "Ele pode ser:\n"
                "  • gerente de algum departamento;\n"
                "  • supervisor de outros empregados;\n"
                "  • alocado em algum projeto (TrabalhaEm);\n"
                "  • responsável por dependentes.\n\n"
                "Remova ou altere esses vínculos antes de excluir."
                "\n\nDetalhe técnico:\n" + str(erro))
        except Exception as erro:
            meu_cursor.rollback()
            QMessageBox.warning(self, "Erro ao excluir", str(erro))

    def cancelar_acao(self):
        self.voltar_a_navegar()
        self.atualizar_tela()  
        self.mensagem.showMessage("Operação cancelada.")

   
    def buscar_registro(self):
        texto, ok = QInputDialog.getText(self, "Buscar empregado",
                                         "Digite o nome (ou parte dele):")
        if ok and texto.strip() != "":
            procurado = texto.strip().lower()
            for indice in range(self.quantos_dados):
                emp = self.dados[indice]
                nome = f"{emp[1]} {emp[2] or ''} {emp[3]}".lower()
                if procurado in nome:
                    self.registro_atual = indice
                    self.atualizar_tela()
                    return
            self.mensagem.showMessage("Nenhum empregado encontrado com esse nome.")

    def mudar_aba(self):
        if self.abas.currentIndex() == 1:   
            try:
                comando = \
                    "SELECT E.cpf, " +\
                    "  E.PreNome+' '+ISNULL(E.InicialMeio+' ','')+E.Sobrenome AS NomeCompleto, " +\
                    "  E.dataNascimento, E.Endereco, E.Sexo, E.Salario, " +\
                    "  ISNULL(D.NomeDepto, '') AS NomeDepto, " +\
                    "  ISNULL(G.PreNome+' '+ISNULL(G.InicialMeio+' ','')+G.Sobrenome, '') AS NomeGerente, " +\
                    "  ISNULL(S.PreNome+' '+ISNULL(S.InicialMeio+' ','')+S.Sobrenome, '') AS NomeSupervisor " +\
                    " FROM V_Emp.Empregado E " +\
                    "   LEFT JOIN V_Emp.Departamento D ON E.NumDepto = D.NumDepto " +\
                    "   LEFT JOIN V_Emp.Empregado G ON D.Gerente_cpf = G.cpf " +\
                    "   LEFT JOIN V_Emp.Empregado S ON E.super_cpf = S.cpf " +\
                    " ORDER BY NomeCompleto"
                result_set = meu_cursor.execute(comando)
                vetor_de_registros = result_set.fetchall()
                numero_de_linhas = len(vetor_de_registros)
                self.tblEmpregado.setRowCount(numero_de_linhas)
                for qual_linha in range(0, numero_de_linhas, 1):
                    emp = vetor_de_registros[qual_linha]
                    
                    for qual_coluna in range(0, 9, 1):
                        valor = emp[qual_coluna]
                        if valor is None:
                            texto = ""
                        elif qual_coluna == 2:   
                            texto = self.para_qdate(valor).toString('dd/MM/yyyy')
                        elif qual_coluna == 5:  
                            texto = f"{float(valor):.2f}"
                        else:
                            texto = str(valor)
                        self.tblEmpregado.setItem(qual_linha, qual_coluna,
                                                  QTableWidgetItem(texto))
                self.tblEmpregado.resizeColumnsToContents()
                self.tblEmpregado.resizeRowsToContents()
                self.mensagem.showMessage(f"Listagem realizada: {numero_de_linhas} empregados.")
            except Exception as erro:
                self.mensagem.showMessage(str(erro))
        else:
            self.preencher_combo_deptos()
            self.atualizar_tela()


conexao = None
meu_cursor = None
aplicacao = QApplication(sys.argv)
dlgCon = DialogoConexao()
if dlgCon.exec() == QDialog.Accepted:
    try:
        conexao = bd.connect(driver="SQL Server",
                             server=f"{dlgCon.edServidor.text()}",
                             database=f"{dlgCon.edBancoDeDados.text()}",
                             uid=f"{dlgCon.edUsuario.text()}",
                             pwd=f"{dlgCon.edSenha.text()}")
        print("Conexão bem sucedida!")
        meu_cursor = conexao.cursor()  
        janela = FormPrincipal()
        aplicacao.exec()
    except Exception as erro:
        print("Não foi possível conectar ao banco de dados:", erro)
    finally:
        if meu_cursor is not None:
            meu_cursor.close()
        if conexao is not None:
            conexao.close()

print("Programa encerrado.")