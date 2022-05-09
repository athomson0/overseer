// Mostly copied from https://stackoverflow.com/a/23352499/17805479
export const timeSince = (timeStamp, short=true) => {
    timeStamp = Date.parse(timeStamp);

    var now = new Date(),
    secondsPast = (now.getTime() - timeStamp) / 1000;
    if(secondsPast < 60){
        return secondsPast + (short ? 's' : 'seconds ago');
    }
    if(secondsPast < 3600){
        return parseInt(secondsPast/60) + (short ? 'm' : ' minutes ago');
    }
    if(secondsPast <= 86400){
        return parseInt(secondsPast/3600) + (short ? 'h' : ' hours ago');
    }
    if(secondsPast <= 2628000){
        return parseInt(secondsPast/86400) + (short ? 'd' : ' days ago');
    }
    if(secondsPast <= 31536000){
        return parseInt(secondsPast/2628000) + (short ? 'mo' : ' months ago');
    }
    if(secondsPast > 31536000){
        return parseInt(secondsPast/31536000) + (short ? 'y' : ' years ago');
    }
}