/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package conexoes;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
//import com.zaxxer.hikari.HikariConfig;
//import com.zaxxer.hikari.HikariDataSource;
/**
 *
 * @author Lucas
 */
public class ConexaoDB {
    
    // URL do banco de dados
    private static final String URL = "jdbc:postgresql://localhost:5432/postgres";
    // Nome de usuário do banco de dados
    private static final String USER = "postgres";
    // Senha do banco de dados
    private static final String PASSWORD = "superfranky123";

     public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }

     
    public static void closeConnection(Connection connection) {
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                System.out.println("Erro ao fechar a conexão: " + e.getMessage());
            }
    
        }
    }
    
    
    public static void main(String[] args) {
        Connection connection = null;

        try {
            // Estabelecendo a conexão
            connection = DriverManager.getConnection(URL, USER, PASSWORD);

            if (connection != null) {
                System.out.println("Conectado ao banco de dados PostgreSQL!");
            } else {
                System.out.println("Falha na conexão com o banco de dados.");
            }
        } catch (SQLException e) {
            System.out.println("Erro ao conectar ao banco de dados: " + e.getMessage());
        } finally {
            // Fechando a conexão
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    System.out.println("Erro ao fechar a conexão: " + e.getMessage());
                }
            }
        }
    }

}
    

