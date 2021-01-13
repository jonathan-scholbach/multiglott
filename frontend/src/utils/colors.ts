export function mixColors(color1, color2, percent: number) {
    var red1 = parseInt(color1[1] + color1[2], 16);
    var green1 = parseInt(color1[3] + color1[4], 16);
    var blue1 = parseInt(color1[5] + color1[6], 16);
  
    var red2 = parseInt(color2[1] + color2[2], 16);
    var green2 = parseInt(color2[3] + color2[4], 16);
    var blue2 = parseInt(color2[5] + color2[6], 16);
  
    var red = Math.round(degree(red1, red2, percent));
    var green = Math.round(degree(green1, green2, percent));
    var blue = Math.round(degree(blue1, blue2, percent));
  
    return hex(red, green, blue);
  }
  
  function hex(r: number, g: number, b:number): string {
    var rString = r.toString(16);
    var gString = g.toString(16);
    var bString = b.toString(16);
  
    while (rString.length < 2) { rString = "0" + rString; }
    while (gString.length < 2) { gString = "0" + gString; }
    while (bString.length < 2) { bString = "0" + bString; }
  
    return "#" + rString + gString + bString;
  }
  
  function degree(start: number, end: number, percent: number): number {
      return start + ((percent) * (end - start));
  }