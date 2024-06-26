const snowflake = require('snowflake-sdk');
const logger = require('../utils/logger');

let connection;

const initialize = (account, username, password) => {
    logger.info('Trying to initialize Snowflake connection');
    connection = snowflake.createConnection({
        account: account,
        username: username,
        password: password
    });

    return new Promise((resolve, reject) => {
        connection.connect((err, conn) => {
            if (err) {
                logger.error(`Failed to connect to Snowflake: ${err.message}`);
                reject(err);
            } else {
                logger.info('Successfully connected to Snowflake');
                resolve(conn);
            }
        });
    });
};

const execute = (query) => {
    logger.info(`Executing query: ${query}`);
    return new Promise((resolve, reject) => {
        connection.execute({
            sqlText: query,
            complete: (err, stmt, rows) => {
                if (err) {
                    logger.error(`Failed to execute query: ${err.message}`);
                    reject(err);
                } else {
                    logger.info('Query executed successfully');
                    resolve(rows);
                }
            }
        });
    });
};

const stop = () => {
    if (connection) {
        logger.info('Closing Snowflake connection');
        connection.destroy();
    }
};

module.exports = {
    initialize,
    execute,
    stop
};
