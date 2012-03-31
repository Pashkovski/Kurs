import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.applet.*;

public class ButtonDemo extends Applet implements ActionListener {

	@Override
	public void actionPerformed(ActionEvent arg0) {
		// TODO Auto-generated method stub
		
	}
	
	String msg="";
	Button but1, but2, but3;
	
/*
class MenuFrame extends Frame {
	String msg="";
	CheckboxMenuItem debug, test;

    MenuFrame(String title) {
    	MenuBar mbar=new MenuBar();
    	setMenuBar(mbar);
    	Menu file=new Menu("File");
    	MenuItem item1, item2, item3, item4, item5;
    	file.add(item1=new MenuItem("New file"));
    	file.add(item2=new MenuItem("Open file"));
    	file.add(item3=new MenuItem("Close file"));
    	file.add(item4=new MenuItem("Blablabla"));
    	file.add(item5=new MenuItem("Quit"));
    	mbar.add(file);
    	
    }
	
} */
public void init() {
	but1=new Button("Text");
	but2=new Button("Text");
	but3=new Button("Text");
	
	add(but1);
	add(but2);
	add(but3);
	
	but1.addActionListener(this);
	but2.addActionListener(this);
	but3.addActionListener(this);
}
}