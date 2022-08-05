import torch
from currency_converter import CurrencyConverter

# Class that does the work of using the model to find coins
class Detector:
    # Base value of each currency in key-value dictionary
    COINS = {
        'Penny': 0.01,
        'Nickel': 0.05,
        'Dime': 0.1,
        'Quarter': 0.25,
        'Half Dollar': 0.50,
        'Dollar': 1.0,
        'Loonie': 1.0,
        'Toonie': 2.0
    }
    
    def __init__(self, model_path, threshold):
        """Initializes Detector class 
        Args:
            model_path: path of the trained a.i. model
            threshold: minimum confidence for object to be identified 
        """
        self.model_path = model_path
        self.threshold = threshold
        
    def load_model(self):
        """Loads the model via Pytorch Hub"""
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', self.model_path) 
        print('Model sucessfully loaded')
        
    def infer(self, img, save_dir):
        """Run inference on the image and save it to the specified directory
        Args:
            img: directory of image to run inference on
            save_dir: directory to save inferenced image to 
        """
        self.model.conf = self.threshold
        self.results = self.model(img, size=416)
        
        # Puts image in a panda matrix so it is compatible with pandas
        self.info = self.results.pandas().xyxy[0]
        print('Inference complete with results: \n{}'.format(self.info))
        
        self.results.save(save_dir=save_dir)
        
    def get_total_amount(self, currency):
        """Calculates the total amount in the desired currency
        Args:
            currency: the desired currency to convert to 
        Returns:
            float: total amount in currency
        """
        # Formats pandas class name column to string seperated by space
        def process_names(data):
            data = data.to_string()
            data = ''.join([i for i in data if i.isalpha() or i == '(' or i == ')'])
            data = data.replace('(', ' (')
            data = data.replace(')', '),')
            data = data[:len(data) - 1]
            
            return data
                
        
        names = process_names(self.info['name'])
        
        names = names.split(',')
        print('names', names)
        self.names_count = {}
        
        #Counts occurences of each unique name
        for i in names:
            if i in self.names_count: self.names_count[i] += 1
            else: self.names_count[i] = 1
        
        coin_vals = {'USD': 0, 'CAD': 0}
        
        #Adds like currency coin values together 
        for key in self.names_count:
            for coin in self.COINS:
                if coin in key:
                    amount = round(self.names_count[key] * self.COINS[coin], 2)
                    if 'CAD' in key:
                        coin_vals['CAD'] += amount
                    else: 
                        coin_vals['USD'] += amount
        
        print('names_count', self.names_count)
        print('coin_vals', coin_vals)
        

        converter = CurrencyConverter()
        converted_amount = 0
        
        #Converts to one currency and add to the amount
        for key in coin_vals:
            converted_amount += converter.convert(coin_vals[key], key, currency)
        
        print('converted money to {} with value {} {}'.format(currency, converted_amount, currency))
        return round(converted_amount, 2);
    # Returns number of coins in image
    def get_num_coins(self):
        return self.names_count
# Thank you Vincent for help with the comments! <3