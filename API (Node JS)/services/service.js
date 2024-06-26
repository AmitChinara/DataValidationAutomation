const pages = require("../details/pages");
const dbmanager = require('../services/snowflakeManager');
const query = require("../details/queries");
const logger = require('../utils/logger');

const getLoginPage = () => {
    return { "logininfo": pages.login_info };
};

const getDataBaseNames = async (accountNo, username, password) => {
    let account;
    switch (accountNo) {
        case 1:
            account = 'wf34578.ap-southeast-1';
            break;
        case 2:
            account = 'link2';
            break;
        default:
            account = 'Link3';
    }

    try {
        logger.info(`Fetching database names for account: ${account}`);
        await dbmanager.initialize(account, username, password);
        return await dbmanager.execute(query.FETCH_DATABASE);
    } catch (error) {
        logger.error(`Error fetching database names: ${error.message}`);
        return { error: error.message };
    } finally {
        dbmanager.stop();
    }
};

const getTableNames = async (accountNo, username, password, database) => {
    let account;
    switch (accountNo) {
        case 1:
            account = 'wf34578.ap-southeast-1';
            break;
        case 2:
            account = 'link2';
            break;
        default:
            account = 'Link3';
    }

    try {
        logger.info(`Fetching table names for database: ${database}`);
        await dbmanager.initialize(account, username, password);
        let prepared_query = query.FETCH_TABLE.replace("{{datbase_name}}", database);
        return await dbmanager.execute(prepared_query);
    } catch (error) {
        logger.error(`Error fetching database names: ${error.message}`);
        return { error: error.message };
    } finally {
        dbmanager.stop();
    }
};

module.exports = {
    getLoginPage,
    getDataBaseNames,
    getTableNames
};
