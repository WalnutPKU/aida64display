#include <U8g2lib.h>

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/U8X8_PIN_NONE);
char line[8][40]; //display string
char data[40];

void refresh()
{
    // Clear Screen
    u8g2.clearBuffer(); 
    // Pick a compatible font for display
    // Default Font size: height 16 * width 8 => 4 lines * 16 characters
    u8g2.setFont(u8g2_font_wqy12_t_gb2312);
    //u8g2.setFont(u8g2_font_unifont_t_symbols);
    // Use drawUTF8(x, y, string) to print unicode string
    // start coordinates is around the bottom-left of the character
    u8g2.drawUTF8(0, 12, line[0]);
    u8g2.drawUTF8(0, 24, line[1]);
    u8g2.drawUTF8(0, 36, line[2]);
    u8g2.drawUTF8(0, 48, line[3]);
    u8g2.drawUTF8(0, 60, line[4]);
    // Print screen
    u8g2.sendBuffer(); 
}

void setup()
{
    // put your setup code here, to run once:
    u8g2.begin();
    u8g2.enableUTF8Print();
    Serial.begin(1500000); // 1500000 as baudrate
}

void loop()
{
    if (Serial.available() > 0)
    {   
        int i = 0;
        // Data Frame format: {nline:data}
        byte t_Byte = Serial.read();
        if (t_Byte == '{')
        {
            i = 0;
            t_Byte = Serial.read();
            int nline = t_Byte - '0'; //get line number
            t_Byte = Serial.read();
            while (t_Byte != '}')
            {
                while (Serial.available() == 0)
                    ;
                t_Byte = Serial.read();
                if (t_Byte != '}')
                {
                    data[i++] = t_Byte;
                }
                else
                {
                    data[i] = '\0'; //end of line
                }
            }
            strcpy(line[nline], data); //write data
            nline = nline + 1;
            refresh();
        }
    }
    
}
