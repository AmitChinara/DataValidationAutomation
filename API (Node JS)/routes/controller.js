var express = require('express');
var router = express.Router();
const service = require('../services/service');
const logger = require('../utils/logger');

router.get('/loginpage', (req, res, next) => {
    logger.info('GET /loginpage');
    res.json(service.getLoginPage());
});

router.post('/fetchdbnames', async (req, res, next) => {
    const { account, username, password } = req.body;
    logger.info(`POST /fetchdbnames with account: ${account}`);

    try {
        const result = await service.getDataBaseNames(account, username, password);
        res.json(result);
    } catch (error) {
        logger.error(`Error in POST /fetchdbnames: ${error.message}`);
        res.status(500).json({ error: error.message });
    }
});

router.post('/fetchtablenames', async (req, res, next) => {
    const { account, username, password, database } = req.body;
    logger.info(`POST /fetchtablenames with database: ${database}`);

    try {
        const result = await service.getTableNames(account, username, password, database);
        res.json(result);
    } catch (error) {
        logger.error(`Error in POST /fetchtablenames: ${error.message}`);
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
