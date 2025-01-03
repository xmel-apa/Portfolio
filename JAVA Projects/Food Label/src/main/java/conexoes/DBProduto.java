package conexoes;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.sql.Timestamp;

public class DBProduto {
    
    public void inserirDadosProdutoValidade(int cod_validade, String data_registro, String data_validade,
            int cod_produto, int cod_categoria, int cod_conservacao, int cod_usuario, int cod_validade2,
            String sif, int lote, String nome_produto, int peso) {
        
        String sqlvalidade = "INSERT INTO validade (cod_validade, data_registro, data_validade) VALUES (?, ?, ?)";
        String sqlproduto = "INSERT INTO produto (cod_produto, cod_categoria, cod_conservacao, cod_usuario, cod_validade, sif, lote, nome_produto, peso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        Connection connection = null;
        PreparedStatement pstmtValidade = null;
        PreparedStatement pstmtProduto = null;
        try {
            
            // Formatar as datas
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
            LocalDate localDateValidade = LocalDate.parse(data_validade, formatter);
            LocalDateTime localDateTimeRegistro = LocalDateTime.parse(data_registro, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

            // Obter conexão do banco de dados
            connection = ConexaoDB.getConnection();
            connection.setAutoCommit(false);

            // Definir valores dos parâmetros
            pstmtValidade = connection.prepareStatement(sqlvalidade);
            pstmtValidade.setInt(1, cod_validade);
            pstmtValidade.setTimestamp(2, Timestamp.valueOf(localDateTimeRegistro));
            pstmtValidade.setDate(3, java.sql.Date.valueOf(localDateValidade));
            pstmtValidade.executeUpdate();
            
            pstmtProduto = connection.prepareStatement(sqlproduto);
            pstmtProduto.setInt(1, cod_produto);
            pstmtProduto.setInt(2, cod_categoria);
            pstmtProduto.setInt(3, cod_conservacao);
            pstmtProduto.setInt(4, cod_usuario);
            pstmtProduto.setInt(5, cod_validade);
            pstmtProduto.setString(6, sif);
            pstmtProduto.setInt(7, lote);
            pstmtProduto.setString(8, nome_produto);
            pstmtProduto.setInt(9, peso);
            pstmtProduto.executeUpdate();
            
            connection.commit();
            System.out.println("Inserções realizadas com sucesso!");

        } catch (SQLException e) {
            // Rollback em caso de erro
            if (connection != null) {
                try {
                    connection.rollback();
                } catch (SQLException rollbackEx) {
                    System.out.println("Erro ao fazer rollback: " + rollbackEx.getMessage());
                }
            }
            System.out.println("Erro ao inserir dados: " + e.getMessage());
        } catch (DateTimeParseException e) {
            System.out.println("Erro ao parsear datas: " + e.getMessage());
        } finally {
            // Fechar PreparedStatements e conexão
            if (pstmtValidade != null) {
                try {
                    pstmtValidade.close();
                } catch (SQLException e) {
                    System.out.println("Erro ao fechar PreparedStatement de validade: " + e.getMessage());
                }
            }
            if (pstmtProduto != null) {
                try {
                    pstmtProduto.close();
                } catch (SQLException e) {
                    System.out.println("Erro ao fechar PreparedStatement de produto: " + e.getMessage());
                }
            }
            ConexaoDB.closeConnection(connection);
        }
    }

    public static void main(String[] args) {
        DBProduto dbprod = new DBProduto();
        // Use a data e hora no formato "yyyy-MM-dd HH:mm:ss" para data_registro
        dbprod.inserirDadosProdutoValidade(1311, "2024-05-29 10:00:00", "2024-05-29", 1030, 3004, 701, 1,1311,"483738", 1321, "Cenoura", 4);
    }
}
