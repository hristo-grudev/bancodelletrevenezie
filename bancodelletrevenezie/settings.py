BOT_NAME = 'bancodelletrevenezie'

SPIDER_MODULES = ['bancodelletrevenezie.spiders']
NEWSPIDER_MODULE = 'bancodelletrevenezie.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'bancodelletrevenezie.pipelines.BancodelletreveneziePipeline': 100,

}